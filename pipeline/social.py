"""Post newly published stories to Bluesky and Mastodon.

Runs after every push to the site branch (.github/workflows/social.yml). A story is
"new" when it is not yet in data/state/social.json; on the very first run everything
already published is recorded without posting, so old stories are never announced.

Accounts are optional and configured with repository secrets:
  BLUESKY_HANDLE, BLUESKY_APP_PASSWORD        (an app password, not the account password)
  MASTODON_INSTANCE, MASTODON_TOKEN           (e.g. https://mastodon.social, token with write:statuses)
Without any account, new stories are recorded as skipped so nothing piles up for later.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "src" / "content"
STATE_PATH = ROOT / "data" / "state" / "social.json"
SITE_URL = "https://datagovernancesignal.com"
USER_AGENT = "DataGovernanceSignal/0.1 (+https://datagovernancesignal.com/about/)"
MAX_POSTS_PER_RUN = 6
WAIT_FOR_LIVE_SECONDS = int(os.environ.get("SOCIAL_WAIT_SECONDS", "900"))

HASHTAGS = {
    "regulation": "DataProtection", "privacy": "Privacy", "ai-governance": "AIGovernance", "strategy": "DataStrategy",
    "data-quality": "DataQuality", "metadata": "Metadata", "mdm": "MDM", "security": "CyberSecurity",
}


# --------------------------------------------------------------------------- content


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def as_date(v) -> date:
    return v if isinstance(v, date) else date.fromisoformat(str(v)[:10])


def published_items(today: date) -> list[dict]:
    """Everything a reader can see on the site today, with what a post needs."""
    items = []
    for kind, folder, url in (("news", "articles", "/news/{}/"), ("opinion", "opinion", "/opinion/{}/"),
                              ("column", "columns", "/monday-signal/{}/")):
        for path in sorted((CONTENT / folder).glob("*.md")):
            d = front_matter(path)
            if not d or d.get("draft") or d.get("sample") or as_date(d["date"]) > today:
                continue
            items.append({
                "key": f"{kind}/{path.stem}",
                "kind": kind,
                "url": SITE_URL + url.format(path.stem),
                "title": d["title"],
                "dek": d.get("dek", ""),
                "categories": d.get("categories", []),
                "thumb": f"{SITE_URL}/cards/thumbs/{path.stem}.png" if kind == "news" else None,
            })
    return items


def shorten(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "…"


def tags(item: dict) -> list[str]:
    out = ["DataGovernance"] + [HASHTAGS[c] for c in item["categories"] if c in HASHTAGS]
    return list(dict.fromkeys(out))[:3]


def label(item: dict) -> str:
    return {"opinion": "Editor's Opinion: ", "column": "The Monday Signal: "}.get(item["kind"], "")


# --------------------------------------------------------------------------- platforms


def bluesky_text(item: dict) -> str:
    """Title and dek within Bluesky's 300 characters; the link travels in the card."""
    head = label(item) + item["title"]
    room = 300 - len(head) - 2
    return head + ("\n\n" + shorten(item["dek"], room) if item["dek"] and room > 40 else "")


def post_bluesky(item: dict, handle: str, password: str) -> str:
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    r = s.post("https://bsky.social/xrpc/com.atproto.server.createSession",
               json={"identifier": handle, "password": password}, timeout=30)
    r.raise_for_status()
    session = r.json()
    auth = {"Authorization": f"Bearer {session['accessJwt']}"}
    external = {"uri": item["url"], "title": item["title"], "description": shorten(item["dek"], 280)}
    if item["thumb"]:
        img = s.get(item["thumb"], timeout=30)
        if img.ok and img.headers.get("Content-Type", "").startswith("image/"):
            up = s.post("https://bsky.social/xrpc/com.atproto.repo.uploadBlob", data=img.content,
                        headers={**auth, "Content-Type": img.headers["Content-Type"]}, timeout=60)
            if up.ok:
                external["thumb"] = up.json()["blob"]
    record = {
        "$type": "app.bsky.feed.post",
        "text": bluesky_text(item),
        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "langs": ["en"],
        "embed": {"$type": "app.bsky.embed.external", "external": external},
    }
    r = s.post("https://bsky.social/xrpc/com.atproto.repo.createRecord", headers=auth, timeout=30,
               json={"repo": session["did"], "collection": "app.bsky.feed.post", "record": record})
    r.raise_for_status()
    return r.json()["uri"]


def mastodon_text(item: dict) -> str:
    """Title, dek, link and hashtags within 500 characters (a link counts as 23)."""
    hashtags = " ".join(f"#{t}" for t in tags(item))
    head = label(item) + item["title"]
    room = 500 - len(head) - 23 - len(hashtags) - 6
    dek = "\n\n" + shorten(item["dek"], room) if item["dek"] and room > 40 else ""
    return f"{head}{dek}\n\n{item['url']}\n\n{hashtags}"


def post_mastodon(item: dict, instance: str, token: str) -> str:
    r = requests.post(
        instance.rstrip("/") + "/api/v1/statuses",
        headers={"Authorization": f"Bearer {token}", "Idempotency-Key": item["key"], "User-Agent": USER_AGENT},
        data={"status": mastodon_text(item), "visibility": "public", "language": "en"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("url", "")


def platforms() -> dict:
    out = {}
    if os.environ.get("BLUESKY_HANDLE") and os.environ.get("BLUESKY_APP_PASSWORD"):
        out["bluesky"] = lambda i: post_bluesky(i, os.environ["BLUESKY_HANDLE"], os.environ["BLUESKY_APP_PASSWORD"])
    if os.environ.get("MASTODON_INSTANCE") and os.environ.get("MASTODON_TOKEN"):
        out["mastodon"] = lambda i: post_mastodon(i, os.environ["MASTODON_INSTANCE"], os.environ["MASTODON_TOKEN"])
    return out


# --------------------------------------------------------------------------- run


def wait_until_live(url: str, seconds: int) -> bool:
    """The site deploys separately; post only once the page answers."""
    deadline = time.monotonic() + seconds
    while True:
        try:
            if requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20).status_code == 200:
                return True
        except requests.RequestException:
            pass
        if time.monotonic() >= deadline:
            return False
        time.sleep(30)


def run(today: date | None = None) -> dict:
    today = today or date.today()
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    state = json.loads(STATE_PATH.read_text(encoding="utf-8")) if STATE_PATH.exists() else None
    items = published_items(today)
    if state is None:  # first run: what is already published is not news to followers
        state = {"since": now, "posted": {i["key"]: {"at": now, "baseline": True} for i in items}}
        STATE_PATH.write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        return {"baseline": len(items), "posted": 0}

    accounts = platforms()
    new = [i for i in items if i["key"] not in state["posted"]]
    summary = {"new": len(new), "posted": 0, "skipped": 0, "failed": 0, "waiting": 0}
    for item in new[:MAX_POSTS_PER_RUN]:
        if not accounts:
            state["posted"][item["key"]] = {"at": now, "skipped": "no accounts configured"}
            summary["skipped"] += 1
            continue
        if not wait_until_live(item["url"], WAIT_FOR_LIVE_SECONDS):
            summary["waiting"] += 1  # not deployed yet: tried again on the next push
            continue
        record = {"at": now}
        for name, post in accounts.items():
            try:
                record[name] = post(item)
            except requests.RequestException as e:
                record[f"{name}_error"] = str(e)[:200]
        if any(k in record for k in accounts):
            state["posted"][item["key"]] = record
            summary["posted"] += 1
        else:
            summary["failed"] += 1  # every platform failed: retried on the next push
        print(f"{item['key']}: {record}")
    STATE_PATH.write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    result = run()
    print(json.dumps(result))
    sys.exit(0)
