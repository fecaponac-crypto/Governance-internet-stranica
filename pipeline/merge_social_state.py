"""Merge two copies of data/state/social.json (ours and the branch's) so no run forgets another's posts.

Usage: python pipeline/merge_social_state.py OURS THEIRS OUT
"""
import json
import sys


def merge(ours: dict, theirs: dict) -> dict:
    posted = {**theirs.get("posted", {})}
    for key, record in ours.get("posted", {}).items():
        # A real post beats a baseline or skip record of the same story.
        if key not in posted or ("bluesky" in record or "mastodon" in record):
            posted[key] = {**posted.get(key, {}), **record}
    return {"since": theirs.get("since") or ours.get("since"), "posted": posted}


if __name__ == "__main__":
    ours, theirs, out = sys.argv[1:4]
    result = merge(json.load(open(ours, encoding="utf-8")), json.load(open(theirs, encoding="utf-8")))
    with open(out, "w", encoding="utf-8") as f:
        f.write(json.dumps(result, indent=1, ensure_ascii=False) + "\n")
