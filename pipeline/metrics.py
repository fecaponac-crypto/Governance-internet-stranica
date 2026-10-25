"""Record this month's key figures in data/metrics/YYYY-MM.json.

Runs after every ingestion run and overwrites the current month's file, so each
month's file ends up holding that month's final figures. Over time this is the
history an advertiser or buyer will ask for.

Always recorded: published articles, collected items, triage and drafting
decisions, editor decisions on drafts, AI spend, source health.
Optional (skipped when the secret is not set):
  BUTTONDOWN_API_KEY                        newsletter subscribers
  CF_API_TOKEN + CF_ACCOUNT_ID + CF_SITE_TAG  Cloudflare Web Analytics visits and page views
"""

from __future__ import annotations

import calendar
import json
import os
import subprocess
from datetime import date, datetime, timezone
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


CF_QUERY = """
query ($account: String!, $filter: AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject) {
  viewer {
    accounts(filter: {accountTag: $account}) {
      rumPageloadEventsAdaptiveGroups(limit: 1, filter: $filter) { count sum { visits } }
    }
  }
}
"""


def web_analytics(start: date, end: date) -> dict | None:
    token, account, site = (os.environ.get(k) for k in ("CF_API_TOKEN", "CF_ACCOUNT_ID", "CF_SITE_TAG"))
    if not (token and account and site):
        return None
    variables = {"account": account, "filter": {"siteTag": site, "date_geq": start.isoformat(), "date_leq": end.isoformat()}}
    try:
        r = requests.post(
            "https://api.cloudflare.com/client/v4/graphql",
            json={"query": CF_QUERY, "variables": variables},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        r.raise_for_status()
        body = r.json()
        if body.get("errors"):
            return {"error": body["errors"][0].get("message", "graphql error")[:200]}
        groups = body["data"]["viewer"]["accounts"][0]["rumPageloadEventsAdaptiveGroups"]
        row = groups[0] if groups else {"count": 0, "sum": {"visits": 0}}
        return {"page_views": row["count"], "visits": row["sum"]["visits"]}
    except (requests.RequestException, KeyError, IndexError, ValueError) as e:
        return {"error": type(e).__name__}


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
    }
    METRICS.mkdir(parents=True, exist_ok=True)
    (METRICS / f"{month}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return record


if __name__ == "__main__":
    print(json.dumps(run(), indent=1))
