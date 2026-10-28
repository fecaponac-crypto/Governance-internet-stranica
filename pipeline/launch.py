"""Public launch: switch off preview mode and remove the sample articles.

Run by .github/workflows/launch.yml (started by the Worker cron shortly before launchAt in
src/data/site.ts). Waits until LEAD_SECONDS before launchAt so the Cloudflare build, which
takes about a minute, goes live at the launch time; the workflow then commits and pushes.

Exit status 0 with "already live" when preview is already off, so a second run does nothing.

Usage: python pipeline/launch.py [--now]   (--now: do not wait for launchAt)
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_TS = ROOT / "src" / "data" / "site.ts"
ARTICLES = ROOT / "src" / "content" / "articles"
LEAD_SECONDS = 60
MAX_WAIT_SECONDS = 15 * 60  # refuse to sit idle longer than this: started on the wrong day


def launch_at(ts: str) -> datetime:
    match = re.search(r"launchAt: '([^']+)'", ts)
    if not match:
        raise SystemExit("launchAt not found in site.ts")
    return datetime.fromisoformat(match.group(1).replace("Z", "+00:00"))


def sample_articles() -> list[Path]:
    out = []
    for path in sorted(ARTICLES.glob("*.md")):
        front = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1])
        if front.get("sample"):
            out.append(path)
    return out


def run(now_flag: bool, sleep=time.sleep, clock=lambda: datetime.now(timezone.utc)) -> str:
    ts = SITE_TS.read_text(encoding="utf-8")
    if re.search(r"^\s+preview: false,", ts, re.M):
        return "already live"
    if not re.search(r"^\s+preview: true,", ts, re.M):
        raise SystemExit("preview flag not found in site.ts")
    if not now_flag:
        wait = (launch_at(ts) - clock()).total_seconds() - LEAD_SECONDS
        if wait > MAX_WAIT_SECONDS:
            raise SystemExit(f"too early: launch is {wait / 60:.0f} minutes away")
        if wait > 0:
            sleep(wait)
    SITE_TS.write_text(re.sub(r"^(\s+)preview: true,", r"\1preview: false,", ts, count=1, flags=re.M), encoding="utf-8")
    removed = sample_articles()
    for path in removed:
        path.unlink()
    return f"launched: preview off, {len(removed)} sample articles removed"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--now", action="store_true", help="launch immediately")
    print(run(parser.parse_args().now))
    sys.exit(0)
