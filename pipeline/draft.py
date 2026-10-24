"""Turn newly collected items into article drafts for editorial review (phase 4).

For items that data/archive marks as "new" and that have not been processed yet:
  1. score relevance and importance in batches with a small model,
  2. fetch the source article for items above the threshold,
  3. write a draft in the portal's format with a stronger model,
  4. open one pull request per draft, assigned to the editor for review.

Nothing is published here: merging the pull request publishes the article.

    python pipeline/draft.py              # full run (needs ANTHROPIC_API_KEY, gh, git)
    python pipeline/draft.py --no-pr      # write drafts to src/content/articles only
    python pipeline/draft.py --score-only # score and record decisions, no drafts

Writes data/state/ai.json (decisions and API spend) and data/reports/drafts.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import requests
import trafilatura
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARTICLES = ROOT / "src" / "content" / "articles"
STATE_PATH = DATA / "state" / "ai.json"
REPORT_PATH = DATA / "reports" / "drafts.md"

SCORER_MODEL = "claude-haiku-5-5"
WRITER_MODEL = "claude-opus-5-5"
# USD per million tokens (input, output); see https://platform.claude.com/docs/en/about-claude/pricing
PRICES = {"claude-haiku-5-5": (0.10, 0.50), "claude-opus-5-5": (4.00, 20.00)}
MONTHLY_BUDGET_USD = float(os.environ.get("AI_MONTHLY_BUDGET_USD", "12"))

SCORE_BATCH = 20
MAX_SCORED_PER_RUN = 120
MAX_DRAFTS_PER_RUN = int(os.environ.get("MAX_DRAFTS_PER_RUN", "6"))
MIN_IMPORTANCE_CORE = 3
MIN_IMPORTANCE_BROAD = 4
MIN_SOURCE_CHARS = 600
MAX_SOURCE_CHARS = 60_000

EDITOR = os.environ.get("EDITOR_GITHUB", "fecaponac-crypto")
USER_AGENT = "Mozilla/5.0 (compatible; DataGovernanceSignal/0.1; +https://datagovernancesignal.com/about/)"
FALLBACK_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


# --------------------------------------------------------------------------- site vocabulary


def site_vocabulary() -> tuple[list[dict], list[str]]:
    """Categories (id, label, section, description) and content types from src/data/site.ts."""
    ts = (ROOT / "src" / "data" / "site.ts").read_text(encoding="utf-8")
    cats = []
    for block in re.findall(r"\{\s*id: '([^']+)',\s*label: '([^']+)',\s*short: '[^']+',\s*section: '(\w+)',\s*description:\s*'([^']+)'", ts):
        cats.append({"id": block[0], "label": block[1], "section": block[2], "description": block[3]})
    types_block = re.search(r"CONTENT_TYPES = \[(.*?)\] as const", ts, re.S)
    assert cats and types_block, "could not read categories/types from site.ts"
    return cats, re.findall(r"'([^']+)'", types_block.group(1))


def existing_articles() -> list[dict]:
    out = []
    for path in sorted(ARTICLES.glob("*.md")):
        front = path.read_text(encoding="utf-8").split("---")[1]
        meta = yaml.safe_load(front)
        out.append({"slug": path.stem, "title": meta["title"], "date": str(meta["date"])})
    return out


# --------------------------------------------------------------------------- state & cost


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"processed": {}, "usage": {}}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def month_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def record_usage(state: dict, model: str, usage) -> float:
    price_in, price_out = PRICES.get(model, PRICES[WRITER_MODEL])
    tokens_in = (usage.input_tokens or 0) + (getattr(usage, "cache_creation_input_tokens", 0) or 0)
    tokens_in += 0.1 * (getattr(usage, "cache_read_input_tokens", 0) or 0)
    cost = tokens_in / 1e6 * price_in + (usage.output_tokens or 0) / 1e6 * price_out
    month = state["usage"].setdefault(month_key(), {"usd": 0.0, "calls": 0})
    month["usd"] = round(month["usd"] + cost, 4)
    month["calls"] += 1
    return cost


def over_budget(state: dict) -> bool:
    return state["usage"].get(month_key(), {}).get("usd", 0.0) >= MONTHLY_BUDGET_USD


# --------------------------------------------------------------------------- model calls


class ModelError(RuntimeError):
    pass


def call_json(client: anthropic.Anthropic, state: dict, *, model: str, system: str, user: str, schema: dict,
              effort: str, max_tokens: int) -> dict:
    params = dict(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
    )
    if model == WRITER_MODEL:
        # Re-run on another model if a safety classifier declines (e.g. a security-incident story).
        response = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **params)
    else:
        response = client.messages.create(**params)
    record_usage(state, response.model, response.usage)
    if response.stop_reason == "refusal":
        raise ModelError(f"refused ({getattr(response.stop_details, 'category', None)})")
    if response.stop_reason == "max_tokens":
        raise ModelError("output truncated at max_tokens")
    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        raise ModelError("no text block in response")
    return json.loads(text)


# --------------------------------------------------------------------------- 1. scoring

SCORE_SYSTEM = """You are the news triage editor of Data Governance Signal, an independent English-language portal for data governance professionals: chief data officers, data governance leads, data stewards, DPOs, compliance, risk and AI governance teams.

Core coverage (categories):
{core}

Broader "Data & AI" coverage, only when it clearly affects how data is governed:
{broad}

For each candidate item decide whether it belongs on the portal and how important it is for practitioners:
1 Background · 2 Worth knowing · 3 Notable · 4 Important (practitioners should act or brief leadership) · 5 Critical (major regulation, landmark decision or enforcement with broad impact).

Rules:
- Relevant: regulation, enforcement, court decisions, regulator guidance, standards, significant research, significant product launches, acquisitions or funding in the governance market, real-world governance practice.
- Not relevant: webinars, event promotion, award announcements, hiring news, generic thought-leadership or vendor marketing, how-to listicles, stories without a data/privacy/AI-governance angle.
- Vendor blog posts are relevant only for genuine launches, acquisitions or research findings.
- If an item reports the same story as one of the existing articles listed below, set same_story_as to that article's slug and relevant to false.
- Judge only from the title, source and excerpt; do not invent details."""


def score_schema(category_ids: list[str]) -> dict:
    return {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "index": {"type": "integer"},
                        "relevant": {"type": "boolean"},
                        "importance": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
                        "categories": {"type": "array", "items": {"type": "string", "enum": category_ids}},
                        "same_story_as": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["index", "relevant", "importance", "categories", "same_story_as", "reason"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["items"],
        "additionalProperties": False,
    }


def score_items(client, state, items: list[dict], categories: list[dict], existing: list[dict]) -> dict[str, dict]:
    fmt = lambda section: "\n".join(f"- {c['id']}: {c['label']} — {c['description']}" for c in categories if c["section"] == section)
    system = SCORE_SYSTEM.format(core=fmt("core"), broad=fmt("broad"))
    schema = score_schema([c["id"] for c in categories])
    recent = "\n".join(f"- {a['slug']}: {a['title']}" for a in existing[-60:])
    results: dict[str, dict] = {}
    for start in range(0, len(items), SCORE_BATCH):
        batch = items[start : start + SCORE_BATCH]
        listing = "\n\n".join(
            f"[{n}] Source: {i['source_name']} (type reliability {i['reliability']}/3)\n"
            f"Title: {i['title']}\nPublished: {(i['published'] or i['first_seen'])[:10]}\nExcerpt: {i['excerpt'] or '(none)'}"
            for n, i in enumerate(batch)
        )
        user = f"Existing articles:\n{recent or '(none)'}\n\nCandidate items:\n\n{listing}"
        data = call_json(client, state, model=SCORER_MODEL, system=system, user=user, schema=schema, effort="low", max_tokens=8000)
        for row in data["items"]:
            if 0 <= row["index"] < len(batch):
                results[batch[row["index"]]["id"]] = row
    return results


def should_draft(score: dict, categories: list[dict]) -> bool:
    if not score["relevant"] or score["same_story_as"]:
        return False
    sections = {c["id"]: c["section"] for c in categories}
    core = any(sections.get(c) == "core" for c in score["categories"])
    return score["importance"] >= (MIN_IMPORTANCE_CORE if core else MIN_IMPORTANCE_BROAD)


# --------------------------------------------------------------------------- 2. source text


def fetch_source(url: str) -> tuple[str, str]:
    """Return (final_url, main text). Raises on failure or when too little text is readable."""
    last = None
    for ua in (USER_AGENT, FALLBACK_USER_AGENT):
        try:
            r = requests.get(url, headers={"User-Agent": ua, "Accept-Language": "en"}, timeout=30)
            if r.status_code >= 400:
                last = f"HTTP {r.status_code}"
                continue
            text = trafilatura.extract(r.text, include_comments=False, include_tables=True) or ""
            if len(text) >= MIN_SOURCE_CHARS:
                return r.url, text
            last = f"only {len(text)} characters readable"
        except requests.RequestException as e:
            last = type(e).__name__
    raise ModelError(f"source not readable: {last}")


# --------------------------------------------------------------------------- 3. writing

WRITE_SYSTEM = """You are the editor of Data Governance Signal, an independent, editor-reviewed briefing for data governance professionals. Write one draft article from the single source provided. A human editor will review it before publication.

Editorial rules:
- Use only facts stated in the source. Do not add facts, numbers, dates or quotes from memory. If the source attributes a claim to someone else, attribute it the same way ("according to …").
- Write in your own words in clear British English. Never copy sentences from the source; short quoted phrases in quotation marks are allowed.
- Vendor or company claims (performance figures, benefits) must be attributed to the company.
- If the source is a secondary report, a vendor's own announcement or an advocacy group, add a one-sentence editor_note saying so; otherwise editor_note is empty.
- Neutral, precise tone. No hype, no clickbait, no exclamation marks.

Fields:
- title: informative headline, max 110 characters.
- dek: one or two sentences (max 260 characters) adding what the headline does not say.
- body: 80–150 words in 2–3 short paragraphs of Markdown, **bold** for at most two key facts. What happened, who, key numbers or obligations, what happens next.
- why_it_matters: 2–4 sentences on the practical consequence for data governance, privacy, compliance or AI governance teams — what they should check or do. This is the portal's main value; be concrete, not generic.
- categories: 1–3 category ids, most relevant first.
- who_should_care: 2–4 roles, e.g. "CDO", "DPO", "Data stewards", "AI governance lead", "Legal & compliance", "CISO".
- importance: 1–5 as defined (1 Background … 5 Critical).
- type: one of the allowed content types.
- region: e.g. "EU", "UK", "US", "Global", or a country.
- card_figure: the single key fact for the news card in large type — a number, amount, deadline, article or standard number, or 1–2 words (max 22 characters).
- card_caption: one line explaining card_figure (max 90 characters).
- source_name: the publisher's name as readers know it.
- source_title: the source article's headline.
- source_is_primary: true only if the source is the original publisher of the decision, document or announcement (regulator, court, standards body, the company itself).
- related: up to 2 slugs from the existing articles that cover a closely related story, else empty.
- review_notes: for the editor only — anything uncertain, simplified or worth verifying (empty if none)."""


def write_schema(category_ids: list[str], types: list[str], slugs: list[str]) -> dict:
    s = lambda **kw: {"type": "string", **kw}
    return {
        "type": "object",
        "properties": {
            "title": s(),
            "dek": s(),
            "body": s(),
            "why_it_matters": s(),
            "categories": {"type": "array", "items": s(enum=category_ids)},
            "who_should_care": {"type": "array", "items": s()},
            "importance": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
            "type": s(enum=types),
            "region": s(),
            "card_figure": s(),
            "card_caption": s(),
            "editor_note": s(),
            "source_name": s(),
            "source_title": s(),
            "source_is_primary": {"type": "boolean"},
            "related": {"type": "array", "items": s(enum=slugs) if slugs else s()},
            "review_notes": s(),
        },
        "required": [
            "title", "dek", "body", "why_it_matters", "categories", "who_should_care", "importance", "type", "region",
            "card_figure", "card_caption", "editor_note", "source_name", "source_title", "source_is_primary", "related",
            "review_notes",
        ],
        "additionalProperties": False,
    }


def write_draft(client, state, item: dict, url: str, text: str, categories, types, existing) -> dict:
    note = ""
    if len(text) > MAX_SOURCE_CHARS:
        text, note = text[:MAX_SOURCE_CHARS], "\n[Source text shortened to the first 60,000 characters.]"
    existing_list = "\n".join(f"- {a['slug']}: {a['title']}" for a in existing[-60:])
    cat_list = "\n".join(f"- {c['id']}: {c['label']} ({c['section']})" for c in categories)
    user = (
        f"Allowed categories:\n{cat_list}\n\nAllowed types: {', '.join(types)}\n\n"
        f"Existing articles (for related):\n{existing_list or '(none)'}\n\n"
        f"Source listed in our catalog as: {item['source_name']} (reliability {item['reliability']}/3)\n"
        f"URL: {url}\nPublished: {(item['published'] or item['first_seen'])[:10]}\n\n"
        f"--- SOURCE TEXT ---\n{text}{note}\n--- END SOURCE TEXT ---"
    )
    return call_json(
        client, state, model=WRITER_MODEL, system=WRITE_SYSTEM, user=user,
        schema=write_schema([c["id"] for c in categories], types, [a["slug"] for a in existing]),
        effort="medium", max_tokens=16000,
    )


def slugify(title: str) -> str:
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", ascii_title.lower())
    slug = "-".join(words)[:70].rstrip("-")
    return slug or "draft"


def unique_slug(title: str, taken: set[str]) -> str:
    base = slugify(title)
    slug, n = base, 2
    while slug in taken:
        slug, n = f"{base}-{n}", n + 1
    return slug


def validate(d: dict) -> list[str]:
    problems = []
    words = len(d["body"].split())
    if not 50 <= words <= 220:
        problems.append(f"body has {words} words")
    if len(d["card_figure"]) > 22:
        problems.append("card_figure longer than 22 characters")
    if len(d["card_caption"]) > 90:
        problems.append("card_caption longer than 90 characters")
    if not d["categories"]:
        problems.append("no categories")
    return problems


def to_markdown(d: dict, item: dict, url: str) -> str:
    q = lambda v: json.dumps(v, ensure_ascii=False)
    lines = [
        "---",
        f"title: {q(d['title'])}",
        f"date: {(item['published'] or item['first_seen'])[:10]}",
        f"dek: {q(d['dek'])}",
        f"whyItMatters: {q(d['why_it_matters'])}",
        f"categories: [{', '.join(dict.fromkeys(d['categories']))}]",
        f"whoShouldCare: [{', '.join(q(r) for r in d['who_should_care'])}]",
        f"importance: {d['importance']}",
        f"type: {q(d['type'])}",
        f"region: {q(d['region'])}",
        "sources:",
        f"  - name: {q(d['source_name'])}",
        f"    title: {q(d['source_title'])}",
        f"    url: {q(url)}",
    ]
    if d["source_is_primary"]:
        lines.append("    primary: true")
    if item.get("via"):
        lines += ["via:", f"  name: {q(item['via']['name'])}", f"  url: {q(item['via']['url'])}"]
    lines += [
        f"related: [{', '.join(d['related'][:2])}]",
        "card:",
        f"  figure: {q(d['card_figure'])}",
        f"  caption: {q(d['card_caption'])}",
        "---",
        "",
        d["body"].strip(),
    ]
    if d["editor_note"].strip():
        note = re.sub(r"^editor['’]s note:\s*", "", d["editor_note"].strip(), flags=re.I)
        lines += ["", f"*Editor's note: {note}*"]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- 4. pull requests


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def open_pull_request(slug: str, markdown: str, d: dict, item: dict, url: str, score: dict, base: str) -> str:
    branch = f"drafts/{slug}"
    git("checkout", "-q", "-b", branch, f"origin/{base}")
    try:
        path = ARTICLES / f"{slug}.md"
        path.write_text(markdown, encoding="utf-8")
        git("add", str(path))
        git("commit", "-q", "-m", f"Draft: {d['title']}\n\nSource: {url}\nTriage: {score['reason']}")
        git("push", "-q", "-u", "origin", branch)
    finally:
        git("checkout", "-q", base)
    labels = {1: "Background", 2: "Worth knowing", 3: "Notable", 4: "Important", 5: "Critical"}
    body = f"""**Merge = publish · Close = reject · edit the file to correct before merging**

**Type:** {d['type']} · {d['region']} · **Importance:** {d['importance']} ({labels[d['importance']]})
**Categories:** {', '.join(d['categories'])}
**Card:** `{d['card_figure']}` — {d['card_caption']}

### {d['title']}
{d['dek']}

{d['body']}

### Why it matters
{d['why_it_matters']}

### Source
- {'✅ Primary: ' if d['source_is_primary'] else ''}[{d['source_name']} — {d['source_title']}]({url})
- Collected from: {item['source_name']} · published {(item['published'] or item['first_seen'])[:10]}
{f"- Editor's note in article: {d['editor_note']}" if d['editor_note'].strip() else ''}

### For the editor
- **Why the triage model picked it:** {score['reason']}
- **Check:** {d['review_notes'] or 'nothing flagged'}

@{EDITOR} — new draft for review.

---
_Drafted automatically by the Data Governance Signal pipeline ({WRITER_MODEL}); not published until merged._
"""
    out = subprocess.run(
        ["gh", "pr", "create", "--base", base, "--head", branch,
         "--title", f"Draft: {d['title']} — Importance {d['importance']}",
         "--body", body, "--reviewer", EDITOR, "--assignee", EDITOR],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    return out.stdout.strip().splitlines()[-1]


# --------------------------------------------------------------------------- run


def load_archive() -> list[dict]:
    items = []
    for path in sorted((DATA / "archive").glob("*.jsonl")):
        items += [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    return items


def load_candidates(state: dict) -> list[dict]:
    items = [i for i in load_archive() if i["status"] == "new" and i["id"] not in state["processed"]]
    items.sort(key=lambda i: i["published"] or i["first_seen"], reverse=True)
    return items


def run(args) -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    state = load_state()
    categories, types = site_vocabulary()
    existing = existing_articles()
    taken = {a["slug"] for a in existing}
    client = anthropic.Anthropic()
    summary = {"run": now, "candidates": 0, "scored": 0, "duplicates": 0, "selected": 0, "drafted": 0, "failed": 0,
               "queued": 0, "budget_stop": False}
    log: list[str] = []

    candidates = load_candidates(state)
    summary["candidates"] = len(candidates)
    for item in [i for i in candidates if i.get("duplicate_of")]:
        state["processed"][item["id"]] = {"at": now, "decision": "duplicate", "of": item["duplicate_of"]}
        summary["duplicates"] += 1
    to_score = [i for i in candidates if not i.get("duplicate_of")][:MAX_SCORED_PER_RUN]

    scores: dict[str, dict] = {}
    if to_score and not over_budget(state):
        scores = score_items(client, state, to_score, categories, existing)
    elif to_score:
        summary["budget_stop"] = True

    for item in to_score:
        score = scores.get(item["id"])
        if not score:
            continue  # left unprocessed: retried next run
        summary["scored"] += 1
        decision = "selected" if should_draft(score, categories) else "skipped"
        state["processed"][item["id"]] = {
            "at": now, "decision": decision, "importance": score["importance"], "relevant": score["relevant"],
            "categories": score["categories"], "reason": score["reason"], "same_story_as": score["same_story_as"] or None,
        }
        summary["selected"] += decision == "selected"

    # Draft queue: everything selected and not yet drafted, including items left over from earlier runs.
    by_id = {i["id"]: i for i in load_archive()}
    queue = [(by_id[k], v) for k, v in state["processed"].items() if v["decision"] == "selected" and k in by_id]
    queue.sort(key=lambda pair: (pair[1]["importance"], pair[0]["published"] or pair[0]["first_seen"]), reverse=True)

    if not args.score_only:
        base = os.environ.get("GITHUB_REF_NAME") or git("rev-parse", "--abbrev-ref", "HEAD")
        if not args.no_pr:
            git("fetch", "-q", "origin", base)
        for item, record in queue[:MAX_DRAFTS_PER_RUN]:
            if over_budget(state):
                summary["budget_stop"] = True  # the rest stays queued
                break
            try:
                url, text = fetch_source(item["url"])
                d = write_draft(client, state, item, url, text, categories, types, existing)
                problems = validate(d)
                if problems:
                    raise ModelError("; ".join(problems))
                slug = unique_slug(d["title"], taken)
                taken.add(slug)
                markdown = to_markdown(d, item, url)
                if args.no_pr:
                    (ARTICLES / f"{slug}.md").write_text(markdown, encoding="utf-8")
                    record.update(decision="drafted", draft=slug)
                else:
                    pr = open_pull_request(slug, markdown, d, item, url, record, base)
                    record.update(decision="drafted", draft=slug, pr=pr)
                summary["drafted"] += 1
                log.append(f"- ✅ **{d['title']}** — importance {d['importance']} · {record.get('pr', slug)}")
            except (ModelError, anthropic.APIError, subprocess.CalledProcessError, json.JSONDecodeError) as e:
                detail = e.stderr.strip()[:200] if isinstance(e, subprocess.CalledProcessError) else str(e)[:200]
                record.update(decision="failed", error=detail)
                summary["failed"] += 1
                log.append(f"- ❌ [{item['title']}]({item['url']}) — {detail}")
        summary["queued"] = max(0, len(queue) - MAX_DRAFTS_PER_RUN)

    save_state(state)
    write_report(state, summary, log)
    return summary


def write_report(state: dict, summary: dict, log: list[str]) -> None:
    month = state["usage"].get(month_key(), {"usd": 0.0, "calls": 0})
    recent = sorted(
        ((k, v) for k, v in state["processed"].items() if v["decision"] in ("skipped", "selected")),
        key=lambda kv: kv[1]["at"], reverse=True,
    )[:15]
    lines = [
        "# Drafts report",
        "",
        f"Last run: **{summary['run']}** · candidates {summary['candidates']} · scored {summary['scored']} · "
        f"selected {summary['selected']} · drafted {summary['drafted']} · failed {summary['failed']} · "
        f"queued for next run {summary['queued']}"
        + (" · ⚠️ monthly AI budget reached" if summary["budget_stop"] else ""),
        "",
        f"AI spend this month: **${month['usd']:.2f}** of ${MONTHLY_BUDGET_USD:.0f} budget ({month['calls']} calls)",
        "",
        "## This run",
        "",
        *(log or ["_No drafts this run._"]),
        "",
        "## Recently skipped by triage",
        "",
        *[f"- ({v.get('importance', '?')}) {v.get('reason', '')}" for _, v in recent if v["decision"] == "skipped"],
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-pr", action="store_true", help="write drafts locally instead of opening pull requests")
    parser.add_argument("--score-only", action="store_true", help="score and record decisions without drafting")
    result = run(parser.parse_args())
    print(json.dumps(result))
    sys.exit(0)
