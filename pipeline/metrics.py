"""Record this month's key figures in data/metrics/YYYY-MM.json.

Runs after every ingestion run and overwrites the current month's file, so each
month's file ends up holding that month's final figures. Over time this is the
history an advertiser or buyer will ask for.

Always recorded: published articles, collected items, triage and drafting
decisions, editor decisions on drafts, AI spend, source health.
Optional (skipped when the secret is not set):
  BUTTONDOWN_API_KEY                        newsletter subscribers
  CF_API_TOKEN + CF_ACCOUNT_ID              Cloudflare Web Analytics: visits, page views, days, top
                                            pages, countries, referrers (CF_SITE_TAG optional:
                                            found automatically); also data/reports/traffic.md
  FEEDBACK_READ_TOKEN                       "Was this useful?" answers (same secret on the Worker)
"""

from __future__ import annotations

import calendar
import json
import os
import subprocess
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARTICLES = ROOT / "src" / "content" / "articles"
METRICS = DATA / "metrics"


def month_bounds(today: date) -> tuple[date, date]:
    last = calendar.monthrange(today.year, today.month)[1]
    return today.replace(day=1), today.replace(day=last)


def articles(month: str) -> dict:
    total = this_month = samples = 0
    by_importance: dict[str, int] = {}
    for path in ARTICLES.glob("*.md"):
        meta = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1])
        if meta.get("sample"):
            samples += 1
            continue
        total += 1
        # Publication month is approximated by the git commit that added the file.
        added = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%cs", "-1", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True,
        ).stdout.strip()
        if added.startswith(month):
            this_month += 1
            key = str(meta.get("importance"))
            by_importance[key] = by_importance.get(key, 0) + 1
    return {"published_total": total, "published_this_month": this_month,
            "published_this_month_by_importance": by_importance, "sample_articles": samples}


def pipeline(month: str) -> dict:
    collected = 0
    archive = DATA / "archive" / f"{month}.jsonl"
    if archive.exists():
        collected = sum(1 for line in archive.read_text(encoding="utf-8").splitlines() if json.loads(line)["status"] == "new")
    runs = [json.loads(l) for l in (DATA / "state" / "runs.jsonl").read_text(encoding="utf-8").splitlines() if l]
    runs = [r for r in runs if r["run"].startswith(month)]
    ai = json.loads((DATA / "state" / "ai.json").read_text(encoding="utf-8")) if (DATA / "state" / "ai.json").exists() else {}
    decisions: dict[str, int] = {}
    for record in ai.get("processed", {}).values():
        if record.get("at", "").startswith(month):
            decisions[record["decision"]] = decisions.get(record["decision"], 0) + 1
    health = json.loads((DATA / "state" / "health.json").read_text(encoding="utf-8"))
    return {
        "items_collected": collected,
        "runs": len(runs),
        "runs_with_failed_sources": sum(1 for r in runs if r["failed"]),
        "triage_decisions": decisions,
        "ai_spend_usd": ai.get("usage", {}).get(month, {}).get("usd", 0.0),
        "sources_active": len(health),
        "sources_failing_now": sum(1 for h in health.values() if h.get("consecutive_failures")),
    }


def editor_decisions(start: date) -> dict | None:
    """Merged and closed draft pull requests this month (needs gh and GH_TOKEN)."""
    def count(state: str) -> int:
        out = subprocess.run(
            ["gh", "pr", "list", "--state", state, "--limit", "500", "--json", "title,mergedAt,closedAt",
             "--search", f"Draft: in:title closed:>={start.isoformat()}"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
        prs = json.loads(out)
        if state == "closed":
            prs = [p for p in prs if not p["mergedAt"]]
        return len(prs)

    try:
        return {"drafts_published": count("merged"), "drafts_rejected": count("closed")}
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def newsletter() -> dict | None:
    key = os.environ.get("BUTTONDOWN_API_KEY")
    if not key:
        return None
    try:
        r = requests.get(
            "https://api.buttondown.com/v1/subscribers",
            params={"type": "regular", "page_size": 1},
            headers={"Authorization": f"Token {key}"},
            timeout=30,
        )
        r.raise_for_status()
        return {"confirmed_subscribers": r.json()["count"]}
    except (requests.RequestException, KeyError, ValueError) as e:
        return {"error": type(e).__name__}


def feedback(month: str) -> dict | None:
    token = os.environ.get("FEEDBACK_READ_TOKEN")
    if not token:
        return None
    try:
        r = requests.get("https://datagovernancesignal.com/api/feedback", params={"month": month},
                         headers={"Authorization": f"Bearer {token}"}, timeout=30)
        r.raise_for_status()
        pages = r.json()["pages"]
    except (requests.RequestException, KeyError, ValueError) as e:
        return {"error": type(e).__name__}
    reasons: dict[str, int] = {}
    for counts in pages.values():
        for reason, n in counts.get("reasons", {}).items():
            reasons[reason] = reasons.get(reason, 0) + n
    return {
        "useful_yes": sum(c.get("yes", 0) for c in pages.values()),
        "useful_no": sum(c.get("no", 0) for c in pages.values()),
        "reasons": reasons,
        "pages": pages,
    }


CF_GRAPHQL = "https://api.cloudflare.com/client/v4/graphql"
SITE_HOST = "datagovernancesignal.com"

# Cloudflare Web Analytics (RUM): real page loads in browsers, no cookies.
CF_SITES = """
query ($account: String!, $filter: AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject) {
  viewer { accounts(filter: {accountTag: $account}) {
    rumPageloadEventsAdaptiveGroups(limit: 50, filter: $filter) { count dimensions { siteTag requestHost } }
  } }
}
"""

CF_QUERY = """
query ($account: String!, $filter: AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject) {
  viewer { accounts(filter: {accountTag: $account}) {
    total: rumPageloadEventsAdaptiveGroups(limit: 1, filter: $filter) { count sum { visits } }
    days: rumPageloadEventsAdaptiveGroups(limit: 31, filter: $filter, orderBy: [date_ASC]) {
      count sum { visits } dimensions { date }
    }
    pages: rumPageloadEventsAdaptiveGroups(limit: 10, filter: $filter, orderBy: [count_DESC]) {
      count dimensions { requestPath }
    }
    countries: rumPageloadEventsAdaptiveGroups(limit: 10, filter: $filter, orderBy: [count_DESC]) {
      count dimensions { countryName }
    }
    referrers: rumPageloadEventsAdaptiveGroups(limit: 10, filter: $filter, orderBy: [count_DESC]) {
      count dimensions { refererHost }
    }
  } }
}
"""


def graphql(token: str, query: str, variables: dict) -> dict:
    r = requests.post(CF_GRAPHQL, json={"query": query, "variables": variables},
                      headers={"Authorization": f"Bearer {token}"}, timeout=30)
    r.raise_for_status()
    body = r.json()
    if body.get("errors"):
        raise ValueError(body["errors"][0].get("message", "graphql error")[:200])
    return body["data"]["viewer"]["accounts"][0]


def find_site_tag(token: str, account: str, start: date, end: date) -> str | None:
    """The Web Analytics site tag for our host, so only the API token and account id are needed."""
    data = graphql(token, CF_SITES, {"account": account, "filter": {"date_geq": start.isoformat(), "date_leq": end.isoformat()}})
    for row in sorted(data["rumPageloadEventsAdaptiveGroups"], key=lambda r: -r["count"]):
        if row["dimensions"]["requestHost"].removeprefix("www.") == SITE_HOST:
            return row["dimensions"]["siteTag"]
    return None


def web_analytics(start: date, end: date) -> dict | None:
    token, account = os.environ.get("CF_API_TOKEN"), os.environ.get("CF_ACCOUNT_ID")
    if not (token and account):
        return None
    try:
        site = os.environ.get("CF_SITE_TAG") or find_site_tag(token, account, start - timedelta(days=60), end)
        if not site:
            return {"page_views": 0, "visits": 0, "note": "no Web Analytics data for the site yet"}
        filt = {"siteTag": site, "date_geq": start.isoformat(), "date_leq": end.isoformat()}
        # Exclude bots, like the dashboard's default view; fall back if the field is not accepted.
        try:
            data, bots_excluded = graphql(token, CF_QUERY, {"account": account, "filter": {**filt, "bot": 0}}), True
        except ValueError:
            data, bots_excluded = graphql(token, CF_QUERY, {"account": account, "filter": filt}), False
    except (requests.RequestException, KeyError, IndexError, ValueError) as e:
        return {"error": str(e)[:200] if isinstance(e, ValueError) else type(e).__name__}
    total = (data["total"] or [{"count": 0, "sum": {"visits": 0}}])[0]
    top = lambda rows, key: [{key: r["dimensions"][key] or "(direct)", "page_views": r["count"]} for r in rows]
    return {
        "page_views": total["count"],
        "visits": total["sum"]["visits"],
        "bots_excluded": bots_excluded,
        "by_day": [{"date": r["dimensions"]["date"], "page_views": r["count"], "visits": r["sum"]["visits"]} for r in data["days"]],
        "top_pages": top(data["pages"], "requestPath"),
        "countries": top(data["countries"], "countryName"),
        "referrers": top(data["referrers"], "refererHost"),
    }


def traffic_report(record: dict) -> str:
    """data/reports/traffic.md: the month's visits at a glance."""
    web = record.get("web") or {}
    lines = [f"# Traffic — {record['month']}", "", f"Updated {record['updated']} · source: Cloudflare Web Analytics (browsers only, no cookies)", ""]
    if not web or "error" in web:
        lines.append(f"_No data: {web.get('error', 'CF_API_TOKEN / CF_ACCOUNT_ID not set')}_")
        return "\n".join(lines) + "\n"
    lines += [f"**{web['visits']} visits · {web['page_views']} page views** this month"
              f"{' (bots excluded)' if web.get('bots_excluded') else ' (bots not excluded)'}", "",
              "_Cloudflare samples page loads, so figures are estimates rounded to tens._", ""]
    if web.get("by_day"):
        lines += ["| Day | Visits | Page views |", "|---|---:|---:|"]
        lines += [f"| {d['date']} | {d['visits']} | {d['page_views']} |" for d in web["by_day"]]
        lines.append("")
    for title, key, field in (("Top pages", "top_pages", "requestPath"), ("Countries", "countries", "countryName"),
                              ("Referrers", "referrers", "refererHost")):
        if web.get(key):
            lines += [f"## {title}", ""] + [f"- {r[field]} — {r['page_views']}" for r in web[key]] + [""]
    fb = record.get("feedback") or {}
    if fb and "error" not in fb:
        lines += ["## Was this useful?", "", f"- Yes {fb['useful_yes']} · No {fb['useful_no']} · reasons: {fb['reasons'] or 'none'}", ""]
    return "\n".join(lines)


def published_between(start: date, end: date) -> list[str]:
    """Titles of real articles first committed between start and end (inclusive)."""
    titles = []
    for path in sorted(ARTICLES.glob("*.md")):
        meta = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1])
        if meta.get("sample"):
            continue
        added = subprocess.run(["git", "log", "--diff-filter=A", "--format=%cs", "-1", "--", str(path)],
                               cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if added and start.isoformat() <= added <= end.isoformat():
            titles.append(meta["title"])
    return titles


def change(now: int, before: int) -> str:
    if not before:
        return "new" if now else "no change"
    pct = round(100 * (now - before) / before)
    return f"{'+' if pct >= 0 else ''}{pct}%"


def weekly_report(today: date, feedback_month: dict | None) -> str | None:
    """data/reports/weekly.md: the 7 days up to yesterday against the 7 before (emailed on Mondays)."""
    end = today - timedelta(days=1)
    start = end - timedelta(days=6)
    week = web_analytics(start, end)
    if week is None:
        return None
    before = web_analytics(start - timedelta(days=7), start - timedelta(days=1)) or {}
    span = f"{start:%-d %b} – {end:%-d %b %Y}"
    lines = [f"Data Governance Signal — week {span}", ""]
    if "error" in week:
        lines.append(f"Traffic figures unavailable: {week['error']}")
    else:
        lines += [
            f"Visits:      {week['visits']}  ({change(week['visits'], before.get('visits', 0))} on the week before: {before.get('visits', 0)})",
            f"Page views:  {week['page_views']}  ({change(week['page_views'], before.get('page_views', 0))} on the week before: {before.get('page_views', 0)})",
            "",
        ]
        for title, key, field in (("Most read", "top_pages", "requestPath"), ("Countries", "countries", "countryName"),
                                  ("Where visitors came from", "referrers", "refererHost")):
            rows = week.get(key) or []
            if rows:
                lines += [f"{title}:"] + [f"  {r['page_views']:>4}  {r[field]}" for r in rows[:5]] + [""]
    published = published_between(start, end)
    lines += [f"Published this week: {len(published)} stories"] + [f"  - {t}" for t in published] + [""]
    if feedback_month and "error" not in feedback_month:
        lines += [f"'Was this useful?' this month: yes {feedback_month['useful_yes']}, no {feedback_month['useful_no']}", ""]
    lines += [
        "Figures are Cloudflare Web Analytics estimates (sampled, bots excluded).",
        "Month so far: https://github.com/fecaponac-crypto/Governance-internet-stranica/blob/claude/data-intelligence-portal-plan-v46ux0/data/reports/traffic.md",
    ]
    return "\n".join(lines) + "\n"


def run(today: date | None = None) -> dict:
    today = today or datetime.now(timezone.utc).date()
    start, end = month_bounds(today)
    month = today.strftime("%Y-%m")
    record = {
        "month": month,
        "updated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "portal": articles(month),
        "pipeline": pipeline(month),
        "editor": editor_decisions(start),
        "newsletter": newsletter(),
        "web": web_analytics(start, min(end, today)),
        "feedback": feedback(month),
    }
    METRICS.mkdir(parents=True, exist_ok=True)
    (METRICS / f"{month}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "reports" / "traffic.md").write_text(traffic_report(record), encoding="utf-8")
    weekly = weekly_report(today, record["feedback"])
    if weekly:
        (DATA / "reports" / "weekly.md").write_text(weekly, encoding="utf-8")
    return record


if __name__ == "__main__":
    print(json.dumps(run(), indent=1))
