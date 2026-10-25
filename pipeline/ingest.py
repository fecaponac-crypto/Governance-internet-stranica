"""Collect new items from the sources in data/sources.yaml into the archive.

Phase 3 of the pipeline: fetch, normalise, de-duplicate and store. No AI and no
publishing happen here. Run from the repository root:

    python pipeline/ingest.py

Outputs (all under data/):
    archive/YYYY-MM.jsonl   one JSON object per collected item, by month first seen
    state/seen.json         id -> date first seen, used to skip known items
    state/health.json       per-source status (last success, errors, counts)
    state/runs.jsonl        one summary line per run (last 500 kept)
    reports/latest.md       human-readable report of new items and source problems
"""

from __future__ import annotations

import calendar
import hashlib
import html
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARCHIVE = DATA / "archive"
STATE = DATA / "state"
REPORTS = DATA / "reports"

USER_AGENT = "Mozilla/5.0 (compatible; DataGovernanceSignal/0.1; +https://datagovernancesignal.com/about/)"
# Some hosts (e.g. Substack) refuse requests from cloud runners with a bot user agent.
FALLBACK_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
TIMEOUT = 25
MAX_AGE_DAYS = 30  # ignore feed items published earlier than this
BASELINE_FRESH_DAYS = 3  # on a source's first run, items this recent still count as new
SEEN_RETENTION_DAYS = 180
SCRAPE_MAX_LINKS = 40
EXCERPT_CHARS = 300  # the repository is public: keep only a short excerpt
DUPLICATE_WINDOW_DAYS = 7
DUPLICATE_THRESHOLD = 0.7
REPORT_HOURS = 48
STALE_DAYS = 45

TRACKING_PARAMS = re.compile(r"^(utm_|mc_|fbclid$|gclid$|msclkid$|_hs|hsCtaTracking$|ref$|cmpid$)", re.I)
STOPWORDS = set(
    "a an the and or of for to in on at by with from as is are be its it this that new how why what into over after".split()
)


# --------------------------------------------------------------------------- helpers


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime | None) -> str | None:
    return dt.isoformat().replace("+00:00", "Z") if dt else None


def parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def canonical_url(url: str) -> str:
    parts = urlsplit(url.strip())
    host = parts.netloc.lower().removeprefix("www.")
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query) if not TRACKING_PARAMS.match(k)])
    path = parts.path.rstrip("/") or "/"
    return urlunsplit(("https", host, path, query, ""))


def item_id(url: str) -> str:
    return hashlib.sha1(canonical_url(url).encode()).hexdigest()[:16]


def clean_text(s: str | None) -> str:
    if not s:
        return ""
    text = BeautifulSoup(s, "html.parser").get_text(" ")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def excerpt(s: str) -> str:
    if len(s) <= EXCERPT_CHARS:
        return s
    cut = s[:EXCERPT_CHARS].rsplit(" ", 1)[0]
    return cut + "…"


def title_tokens(title: str) -> set[str]:
    words = re.findall(r"[a-z0-9€$£]+", title.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 1}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def keyword_regex(keywords: list[str]) -> re.Pattern[str]:
    alternatives = "|".join(re.escape(k) for k in sorted(keywords, key=len, reverse=True))
    return re.compile(rf"\b(?:{alternatives})\b", re.I)


def read_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- fetching


@dataclass
class Candidate:
    url: str
    title: str
    published: datetime | None
    summary: str = ""


@dataclass
class FetchResult:
    source_id: str
    candidates: list[Candidate] = field(default_factory=list)
    error: str | None = None


session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en"})


def get(url: str) -> requests.Response:
    last: Exception | None = None
    for attempt in range(2):
        try:
            r = session.get(url, timeout=TIMEOUT)
            if r.status_code == 403:
                r = session.get(url, timeout=TIMEOUT, headers={"User-Agent": FALLBACK_USER_AGENT})
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            last = e
            time.sleep(2 * (attempt + 1))
    assert last is not None
    raise last


def entry_date(entry) -> datetime | None:
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        t = entry.get(key)
        if t:
            return datetime.fromtimestamp(calendar.timegm(t), timezone.utc)
    return None


def fetch_rss(source: dict) -> list[Candidate]:
    out: list[Candidate] = []
    for feed_url in source["feeds"]:
        parsed = feedparser.parse(get(feed_url).content)
        if not parsed.entries and parsed.bozo:
            raise ValueError(f"unreadable feed {feed_url}: {parsed.bozo_exception}")
        for e in parsed.entries:
            link = e.get("link")
            title = clean_text(e.get("title"))
            if not link or not title:
                continue
            summary = clean_text(e.get("summary") or e.get("description"))
            out.append(Candidate(urljoin(feed_url, link), title, entry_date(e), summary))
    return out


def scrape_page(html: bytes, page_url: str, rules: dict) -> list[Candidate]:
    """Article links on a listing page.

    rules: link_pattern, optional exclude; optional rewrite {from, to} (regex applied to each
    resolved URL, for sites whose relative links resolve to a wrong path); optional item, a CSS
    selector for one listing entry, whose text becomes the candidate's summary.
    """
    pattern = re.compile(rules["link_pattern"])
    exclude = re.compile(rules["exclude"]) if rules.get("exclude") else None
    rewrite = rules.get("rewrite")
    # Bytes, so BeautifulSoup honours the page's declared charset.
    soup = BeautifulSoup(html, "html.parser")
    containers = soup.select(rules["item"]) if rules.get("item") else [soup]
    found: dict[str, Candidate] = {}
    for container in containers:
        summary = clean_text(container.get_text(" "))[:600] if rules.get("item") else ""
        for a in container.find_all("a", href=True):
            url = urljoin(page_url, a["href"]).split("#")[0]
            if rewrite:
                url = re.sub(rewrite["from"], rewrite["to"], url)
            if not pattern.search(url) or (exclude and exclude.search(url)):
                continue
            title = clean_text(a.get_text(" "))
            # Keep the longest anchor text seen for a URL (cards often repeat the link).
            if url not in found or len(title) > len(found[url].title):
                found[url] = Candidate(url, title, None, summary)
            if len(found) >= SCRAPE_MAX_LINKS:
                return list(found.values())
    return list(found.values())


def fetch_scrape(source: dict) -> list[Candidate]:
    page = get(source["url"])
    found = scrape_page(page.content, page.url, source["scrape"])
    if not found:
        raise ValueError("no article links matched link_pattern — page layout may have changed")
    return [c for c in found if len(c.title) >= 15]


def fetch(source: dict) -> FetchResult:
    try:
        fetcher = fetch_rss if source["method"] == "rss" else fetch_scrape
        return FetchResult(source["id"], fetcher(source))
    except Exception as e:  # one broken source must not stop the run
        return FetchResult(source["id"], error=f"{type(e).__name__}: {e}"[:300])


# --------------------------------------------------------------------------- run


def load_recent_items(days: int) -> list[dict]:
    cutoff = now_utc() - timedelta(days=days)
    items: list[dict] = []
    for path in sorted(ARCHIVE.glob("*.jsonl"))[-2:]:
        for line in path.read_text(encoding="utf-8").splitlines():
            item = json.loads(line)
            if parse_iso(item["first_seen"]) >= cutoff:
                items.append(item)
    return items


def run() -> dict:
    started = now_utc()
    catalog = yaml.safe_load((DATA / "sources.yaml").read_text(encoding="utf-8"))
    sources = [s for s in catalog["sources"] if s.get("active", True) and s["method"] in ("rss", "scrape")]
    keywords = keyword_regex(catalog["keywords"])

    seen: dict[str, str] = read_json(STATE / "seen.json", {})
    health: dict[str, dict] = read_json(STATE / "health.json", {})
    recent = load_recent_items(DUPLICATE_WINDOW_DAYS)
    recent_tokens = [(i["id"], i["source_id"], title_tokens(i["title"])) for i in recent]

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(fetch, sources))

    by_id = {s["id"]: s for s in sources}
    new_items: list[dict] = []
    stats = {"sources": len(sources), "failed": 0, "fetched": 0, "too_old": 0, "known": 0, "filtered": 0, "new": 0, "baseline": 0}
    max_age = started - timedelta(days=MAX_AGE_DAYS)

    for result in results:
        source = by_id[result.source_id]
        h = health.setdefault(source["id"], {"total_items": 0, "consecutive_failures": 0})
        first_run = "last_success" not in h
        h["last_run"] = iso(started)

        if result.error:
            stats["failed"] += 1
            h["consecutive_failures"] += 1
            h["last_error"] = result.error
            continue

        h["consecutive_failures"] = 0
        h["last_success"] = iso(started)
        h.pop("last_error", None)
        stats["fetched"] += len(result.candidates)
        added = 0

        for c in result.candidates:
            if c.published and c.published < max_age:
                stats["too_old"] += 1
                continue
            iid = item_id(c.url)
            if iid in seen:
                stats["known"] += 1
                continue
            seen[iid] = started.date().isoformat()

            text = f"{c.title} {c.summary}"
            if source.get("filter") and not keywords.search(text):
                stats["filtered"] += 1
                continue

            tokens = title_tokens(c.title)
            duplicate_of = next(
                (oid for oid, sid, t in recent_tokens if sid != source["id"] and jaccard(tokens, t) >= DUPLICATE_THRESHOLD),
                None,
            )
            # A source's first successful run only establishes what already exists,
            # except for the last few days' items, so a newly added source contributes at once.
            fresh = c.published is not None and c.published >= started - timedelta(days=BASELINE_FRESH_DAYS)
            status = "baseline" if first_run and not fresh else "new"
            item = {
                "id": iid,
                "source_id": source["id"],
                "source_name": source["name"],
                "section": source["section"],
                "categories": source["categories"],
                "priority": source["priority"],
                "reliability": source["reliability"],
                "title": c.title,
                "url": c.url,
                "published": iso(c.published),
                "first_seen": iso(started),
                "excerpt": excerpt(c.summary),
                "method": source["method"],
                "duplicate_of": duplicate_of,
                "status": status,
            }
            new_items.append(item)
            recent_tokens.append((iid, source["id"], tokens))
            stats[status] += 1
            added += 1

        h["last_item_count"] = added
        h["total_items"] += added
        if added:
            h["last_new_item"] = iso(started)

    # Persist archive, state, run log and report.
    if new_items:
        ARCHIVE.mkdir(parents=True, exist_ok=True)
        with (ARCHIVE / f"{started:%Y-%m}.jsonl").open("a", encoding="utf-8") as f:
            for item in new_items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    cutoff = (started - timedelta(days=SEEN_RETENTION_DAYS)).date().isoformat()
    seen = {k: v for k, v in seen.items() if v >= cutoff}
    write_json(STATE / "seen.json", seen)
    write_json(STATE / "health.json", health)

    summary = {"run": iso(started), "seconds": int((now_utc() - started).total_seconds()), **stats}
    runs_path = STATE / "runs.jsonl"
    runs = runs_path.read_text(encoding="utf-8").splitlines() if runs_path.exists() else []
    runs = (runs + [json.dumps(summary)])[-500:]
    runs_path.write_text("\n".join(runs) + "\n", encoding="utf-8")

    write_report(catalog, health, summary)
    return summary


# --------------------------------------------------------------------------- report


def write_report(catalog: dict, health: dict, summary: dict) -> None:
    started = parse_iso(summary["run"])
    assert started is not None
    items = [i for i in load_recent_items(REPORT_HOURS / 24 + 1) if i["status"] == "new"]
    items = [i for i in items if parse_iso(i["first_seen"]) >= started - timedelta(hours=REPORT_HOURS)]
    items.sort(key=lambda i: i["published"] or i["first_seen"], reverse=True)  # newest first within each group

    lines = [
        "# Inflow report",
        "",
        f"Last run: **{summary['run']}** · sources checked: {summary['sources']} · "
        f"failed: {summary['failed']} · new items this run: {summary['new']}"
        + (f" · baseline items: {summary['baseline']}" if summary["baseline"] else ""),
        "",
        f"## New items, last {REPORT_HOURS} hours ({len(items)})",
        "",
    ]
    if not items:
        lines += ["_No new items._", ""]
    for prio in ("high", "medium", "low"):
        group = [i for i in items if i["priority"] == prio]
        if not group:
            continue
        lines += [f"### {prio.capitalize()} priority sources", "", "| Date | Source | Title |", "|---|---|---|"]
        for i in group:
            date = (i["published"] or i["first_seen"])[:10]
            dup = " _(possible duplicate)_" if i["duplicate_of"] else ""
            title = i["title"].replace("|", "\\|")
            lines.append(f"| {date} | {i['source_name']} | [{title}]({i['url']}){dup} |")
        lines.append("")

    sources = {s["id"]: s for s in catalog["sources"]}
    problems = []
    for sid, h in sorted(health.items()):
        if sid not in sources:
            continue
        name = sources[sid]["name"]
        if h.get("consecutive_failures", 0) >= 1:
            problems.append(f"- **{name}** — failed {h['consecutive_failures']}× in a row: `{h.get('last_error', '')}`")
        elif h.get("last_new_item") and parse_iso(h["last_new_item"]) < started - timedelta(days=STALE_DAYS):
            problems.append(f"- **{name}** — no new items for more than {STALE_DAYS} days")
    lines += ["## Source problems", ""] + (problems or ["_None._"])

    manual = [s for s in catalog["sources"] if s.get("active", True) and s["method"] == "manual"]
    lines += ["", "## Check manually (weekly)", ""] + [f"- [{s['name']}]({s['url']})" for s in manual]

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    result = run()
    print(json.dumps(result))
    # Fail the job only if every source failed (likely a network problem on the runner).
    sys.exit(1 if result["failed"] == result["sources"] else 0)
