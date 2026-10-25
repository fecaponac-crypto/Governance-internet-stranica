"""Prepare The Monday Signal: a column package for the editor, as a pull request.

Runs on Monday morning (Cloudflare Cron dispatches .github/workflows/monday.yml).
The package contains:
  - a draft column (src/content/columns/YYYY-MM-DD.md) based on the articles the editor
    published in the last 7 days, for the editor to rewrite in their own voice;
  - proposed predictions, ours and other people's (appended to data/predictions.yaml);
    another person's prediction is kept only if its quoted words appear in the source text;
  - the open predictions that fall due, for the editor to judge;
  - the newsletter text to paste into Buttondown once the column is published.

Merge = publish the column and the predictions. Close = skip this week.

Usage: python pipeline/monday.py [--date YYYY-MM-DD] [--no-pr]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone

import anthropic
import yaml

import draft
from draft import ARTICLES, EDITOR, ROOT, WRITER_MODEL, ModelError

COLUMNS = ROOT / "src" / "content" / "columns"
PREDICTIONS = ROOT / "data" / "predictions.yaml"
SITE_URL = "https://datagovernancesignal.com"
COLUMN_NAME = "The Monday Signal"

MAX_ARTICLES = 10
MAX_SOURCE_CHARS = 12_000
DUE_WITHIN_DAYS = 7


# --------------------------------------------------------------------------- inputs


def front_matter(text: str) -> tuple[dict, str]:
    _, front, body = text.split("---", 2)
    return yaml.safe_load(front), body.strip()


def added_on(path) -> date | None:
    out = draft.git("log", "--diff-filter=A", "--format=%cs", "-1", "--", str(path)).strip()
    return date.fromisoformat(out) if out else None


def week_articles(monday: date) -> list[dict]:
    """Articles the editor published (merged) in the 7 days before this Monday, most important first."""
    start = monday - timedelta(days=7)
    found = []
    for path in ARTICLES.glob("*.md"):
        meta, body = front_matter(path.read_text(encoding="utf-8"))
        if meta.get("sample") or meta.get("draft"):
            continue
        published = added_on(path)
        if published and start <= published < monday:
            found.append({"slug": path.stem, "meta": meta, "body": body, "published": published})
    found.sort(key=lambda a: (-a["meta"]["importance"], a["slug"]))
    return found[:MAX_ARTICLES]


def load_predictions() -> tuple[str, list[dict]]:
    text = PREDICTIONS.read_text(encoding="utf-8")
    header = "".join(line for line in text.splitlines(keepends=True) if line.startswith("#"))
    return header, yaml.safe_load(text) or []


def due_predictions(predictions: list[dict], monday: date) -> list[dict]:
    limit = monday + timedelta(days=DUE_WITHIN_DAYS)
    return [p for p in predictions if p.get("status", "open") == "open" and p["due"] <= limit]


def source_texts(articles: list[dict]) -> list[dict]:
    """One source per article: the primary source when there is one, else the first."""
    sources = []
    for i, a in enumerate(articles, 1):
        refs = a["meta"]["sources"]
        src = next((s for s in refs if s.get("primary")), refs[0])
        try:
            text = draft.fetch_source(src["url"])["text"][:MAX_SOURCE_CHARS]
        except Exception as e:  # noqa: BLE001 - an unreachable source just means less material
            print(f"  source unavailable ({type(e).__name__}): {src['url']}", file=sys.stderr)
            text = ""
        sources.append({"ref": i, "name": src["name"], "title": src["title"], "url": src["url"], "text": text})
    return sources


# --------------------------------------------------------------------------- writing

SYSTEM = f"""You draft "{COLUMN_NAME}", the weekly column of Data Governance Signal, an independent, editor-reviewed briefing for data governance professionals. The editor writes as "The Steward", a practitioner in master data management since 2011 and data governance since 2019, with governance leadership and AI governance roles. The editor will rewrite your draft in their own voice before publishing, so give them a strong, accurate starting point, not finished prose.

The column:
- Opens with the one development of the week that matters most and says plainly what it means for practitioners.
- Connects the week's stories: patterns, tensions, what changed. Opinion is welcome but must be labelled as such ("I think", "my read") and argued from the facts given.
- Includes a short "What I'm watching" section that states 2-4 predictions of our own, each specific, checkable, with a date.
- If predictions are due for judging, mentions them in a short "Scorecard" paragraph without deciding the outcome (the editor judges).
- 600-900 words of Markdown body, short paragraphs, a few ## subheadings, no title heading.
- Links to our articles as [text](/news/<slug>/). Never invent facts, figures, quotes, names or events beyond the material given. If a point would benefit from the editor's own experience, leave a marker like [EDITOR: add an example from practice].
- British English, no hype, no clichés.

Also extract predictions made by others: forward-looking claims by named actors (regulators, companies, analysts, officials) found in the numbered source texts. Each must quote the exact words from that source text (copied verbatim, at most 40 words), name who made it, and have a date by which it can be judged (use the date stated in the claim, or a reasonable one, e.g. the end of the stated period). Skip vague or unattributed statements. Return none if there are none."""


def schema(source_refs: list[int], due_ids: list[str]) -> dict:
    date_str = {"type": "string", "description": "YYYY-MM-DD"}
    return {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "dek": {"type": "string", "description": "One sentence."},
            "body": {"type": "string"},
            "our_predictions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "claim": {"type": "string"},
                        "due": date_str,
                        "confidence": {"type": "integer", "description": "1-99, % likely"},
                        "reasoning": {"type": "string"},
                    },
                    "required": ["claim", "due", "confidence", "reasoning"],
                    "additionalProperties": False,
                },
            },
            "others_predictions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "claim": {"type": "string"},
                        "by": {"type": "string"},
                        "role": {"type": "string"},
                        "quote": {"type": "string"},
                        "source": {"type": "integer", "enum": source_refs or [0]},
                        "due": date_str,
                    },
                    "required": ["claim", "by", "role", "quote", "source", "due"],
                    "additionalProperties": False,
                },
            },
            "scorecard_hints": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "enum": due_ids or ["none"]},
                        "hint": {"type": "string", "description": "What the material suggests about the outcome, or 'no evidence in this week's material'."},
                    },
                    "required": ["id", "hint"],
                    "additionalProperties": False,
                },
            },
            "review_notes": {"type": "string"},
        },
        "required": ["title", "dek", "body", "our_predictions", "others_predictions", "scorecard_hints", "review_notes"],
        "additionalProperties": False,
    }


def material(monday: date, articles: list[dict], sources: list[dict], due: list[dict]) -> str:
    parts = [f"Column date: {monday.isoformat()} (Monday). Week covered: the 7 days before.\n\n# This week's published articles"]
    for a in articles:
        m = a["meta"]
        parts.append(
            f"## /news/{a['slug']}/ — importance {m['importance']} — {m['type']}\n"
            f"Title: {m['title']}\nDek: {m['dek']}\nWhy it matters: {m['whyItMatters']}\n\n{a['body']}"
        )
    parts.append("# Source texts (for others' predictions)")
    for s in sources:
        parts.append(f"[{s['ref']}] {s['name']} — {s['title']}\n{s['text'] or '(not available)'}")
    if due:
        parts.append("# Predictions due for judging")
        for p in due:
            parts.append(f"- {p['id']}: {p['claim']} (by {p['by']}, due {p['due']})")
    return "\n\n".join(parts)


def normalize(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def verified_others(proposed: list[dict], sources: list[dict]) -> tuple[list[dict], list[dict]]:
    """Keep only predictions whose quote appears word for word in the cited source text."""
    by_ref = {s["ref"]: s for s in sources}
    kept, dropped = [], []
    for p in proposed:
        src = by_ref.get(p["source"])
        quote = normalize(p["quote"].strip(' "'))
        if src and quote and quote in normalize(src["text"]):
            kept.append({**p, "source": src})
        else:
            dropped.append(p)
    return kept, dropped


def valid_date(value: str, after: date) -> date | None:
    try:
        d = date.fromisoformat(value)
    except ValueError:
        return None
    return d if d > after else None


# --------------------------------------------------------------------------- output


def column_markdown(monday: date, col: dict) -> str:
    front = {"title": col["title"], "date": monday, "dek": col["dek"]}
    return "---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000) + "---\n\n" + col["body"].strip() + "\n"


def new_predictions(monday: date, col: dict, others: list[dict]) -> list[dict]:
    url = f"{SITE_URL}/monday-signal/{monday.isoformat()}/"
    out = []
    for p in col["our_predictions"]:
        due = valid_date(p["due"], monday)
        if due:
            out.append({"claim": p["claim"], "by": "Data Governance Signal", "ours": True,
                        "source": {"title": f"{COLUMN_NAME}: {col['title']}", "url": url},
                        "made": monday, "due": due, "confidence": min(99, max(1, p["confidence"]))})
    for p in others:
        due = valid_date(p["due"], monday)
        if due:
            out.append({"claim": p["claim"], "by": p["by"], **({"role": p["role"]} if p["role"].strip() else {}),
                        "quote": p["quote"].strip(' "'), "source": {"title": p["source"]["title"], "url": p["source"]["url"]},
                        "made": monday, "due": due})
    for i, p in enumerate(out, 1):
        p["id"] = f"{monday.isoformat()}-{i}"
        p["status"] = "open"
    return [{"id": p.pop("id"), **p} for p in out]


def predictions_yaml(header: str, predictions: list[dict]) -> str:
    return header + yaml.safe_dump(predictions, sort_keys=False, allow_unicode=True, width=1000)


def newsletter_text(monday: date, col: dict, articles: list[dict]) -> str:
    url = f"{SITE_URL}/monday-signal/{monday.isoformat()}/"
    lines = [f"# {col['title']}", "", col["dek"], "", f"**[Read this week's column →]({url})**", "", "## The week's top stories", ""]
    for a in articles:
        m = a["meta"]
        lines += [f"**[{m['title']}]({SITE_URL}/news/{a['slug']}/)**  ", f"{m['dek']} *Why it matters:* {m['whyItMatters']}", ""]
    lines += ["All predictions, ours and others', are tracked at "
              f"[datagovernancesignal.com/predictions]({SITE_URL}/predictions/)."]
    return "\n".join(lines)


def pr_body(monday: date, col: dict, articles, new: list[dict], dropped, due, hints) -> str:
    hint_by_id = {h["id"]: h["hint"] for h in hints}
    ours = [p for p in new if p.get("ours")]
    others = [p for p in new if not p.get("ours")]
    lines = [
        "**Merge = publish the column and its predictions · Close = skip this week**",
        "",
        f"Draft column for {monday:%A %-d %B %Y}, based on {len(articles)} article(s) published last week. "
        "It is a starting point: **rewrite it in your own voice** (edit "
        f"`src/content/columns/{monday.isoformat()}.md` in this PR), check every claim, fill the `[EDITOR: …]` markers.",
        "",
        "### Our predictions (in `data/predictions.yaml`)",
        "Keep, edit or delete. Once published, they are never edited — only judged.",
    ]
    lines += [f"- **{p['confidence']}%** by {p['due']}: {p['claim']}" for p in ours] or ["- none proposed"]
    lines += ["", "### Others' predictions found in last week's sources (quote verified in the source text)"]
    lines += [f"- **{p['by']}**: {p['claim']} (due {p['due']}) — “{p['quote']}” [source]({p['source']['url']})" for p in others] or ["- none found"]
    if dropped:
        lines += ["", f"<details><summary>{len(dropped)} proposed prediction(s) dropped: quote not found in the source</summary>", ""]
        lines += [f"- {p['by']}: {p['claim']} — “{p['quote']}”" for p in dropped]
        lines += ["", "</details>"]
    lines += ["", "### Predictions due — judge them"]
    if due:
        lines.append("For each: set `status` (correct / partly / wrong / void), `resolved`, `evidence` and optionally `note` in `data/predictions.yaml`, or leave open.")
        lines += [f"- `{p['id']}` ({p['by']}, due {p['due']}): {p['claim']}\n  - hint: {hint_by_id.get(p['id'], '—')}" for p in due]
    else:
        lines.append("- none this week")
    lines += [
        "", "### Newsletter (after merging)",
        "Once the site has rebuilt, paste this into a new Buttondown email and send it:",
        "", "<details><summary>Newsletter text</summary>", "", "```markdown", newsletter_text(monday, col, articles), "```", "", "</details>",
        "", "### For the editor", f"- **Writer's notes:** {col['review_notes'] or 'nothing flagged'}",
        "", f"@{EDITOR} — this week's Monday Signal package.",
        "", "---", f"_Drafted automatically by the Data Governance Signal pipeline ({WRITER_MODEL}); not published until merged._",
    ]
    return "\n".join(lines)


def branch_exists(branch: str) -> bool:
    return bool(draft.git("ls-remote", "--heads", "origin", branch).strip())


def open_pull_request(monday: date, files: dict, title: str, body: str, base: str) -> str:
    branch = f"columns/{monday.isoformat()}"
    draft.git("checkout", "-q", "-b", branch, f"origin/{base}")
    try:
        for path, text in files.items():
            path.write_text(text, encoding="utf-8")
            draft.git("add", str(path))
        draft.git("commit", "-q", "-m", f"Monday Signal draft: {title}")
        draft.git("push", "-q", "-u", "origin", branch)
    finally:
        draft.git("checkout", "-q", base)
    out = subprocess.run(
        ["gh", "pr", "create", "--base", base, "--head", branch, "--title", f"Monday Signal {monday.isoformat()}: {title}",
         "--body", body, "--reviewer", EDITOR, "--assignee", EDITOR],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    return out.stdout.strip().splitlines()[-1]


# --------------------------------------------------------------------------- run


def run(args) -> dict:
    monday = date.fromisoformat(args.date) if args.date else datetime.now(timezone.utc).date()
    if monday.weekday() != 0:
        return {"skipped": f"{monday} is not a Monday"}
    column_path = COLUMNS / f"{monday.isoformat()}.md"
    if column_path.exists() or (not args.no_pr and branch_exists(f"columns/{monday.isoformat()}")):
        return {"skipped": "column package already exists"}

    articles = week_articles(monday)
    if not articles:
        return {"skipped": "no articles published last week"}
    header, predictions = load_predictions()
    due = due_predictions(predictions, monday)

    state = draft.load_state()
    if draft.over_budget(state):
        return {"skipped": "monthly AI budget reached"}
    sources = source_texts(articles)
    client = anthropic.Anthropic()
    try:
        col = draft.call_json(
            client, state, model=WRITER_MODEL, system=SYSTEM, user=material(monday, articles, sources, due),
            schema=schema([s["ref"] for s in sources], [p["id"] for p in due]), effort="medium", max_tokens=16000,
        )
    finally:
        draft.save_state(state)

    others, dropped = verified_others(col["others_predictions"], sources)
    new = new_predictions(monday, col, others)
    files = {column_path: column_markdown(monday, col), PREDICTIONS: predictions_yaml(header, predictions + new)}
    body = pr_body(monday, col, articles, new, dropped, due, col["scorecard_hints"])
    summary = {"column": column_path.name, "articles": len(articles), "predictions": len(new),
               "dropped": len(dropped), "due": len(due)}
    if args.no_pr:
        COLUMNS.mkdir(parents=True, exist_ok=True)
        for path, text in files.items():
            path.write_text(text, encoding="utf-8")
        print(body)
    else:
        base = draft.git("rev-parse", "--abbrev-ref", "HEAD").strip()
        summary["pr"] = open_pull_request(monday, files, col["title"], body, base)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--date", help="column date (a Monday), default today (UTC)")
    parser.add_argument("--no-pr", action="store_true", help="write the files locally instead of opening a pull request")
    try:
        print(run(parser.parse_args()))
    except ModelError as e:
        sys.exit(f"model error: {e}")
