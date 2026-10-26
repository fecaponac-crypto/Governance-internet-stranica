import json
import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import yaml

import draft
import monday
from test_draft import response

MONDAY = date(2026, 11, 2)
SOURCE_TEXT = "The Commission said it expects to adopt the guidelines on high-risk systems by February 2027, after consultation."

COLUMN = {
    "title": "Guidelines are coming, and so is the deadline",
    "dek": "The week's news points one way: high-risk AI obligations are getting concrete.",
    "body": "## The week\n\nIt was a busy week, see [the story](/news/one/).",
    "big_signal": "two",
    "in_practice": "Teams should map where AI touches personal data.",
    "insight_suggestion": "Start the AI inventory from the data catalogue.",
    "our_predictions": [
        {"claim": "At least one DPA will fine an AI deployer by June 2027.", "due": "2027-06-30", "confidence": 65, "reasoning": "x"},
        {"claim": "Bad date", "due": "2020-01-01", "confidence": 50, "reasoning": "x"},
    ],
    "others_predictions": [
        {"claim": "Guidelines adopted by February 2027", "by": "European Commission", "role": "EU executive",
         "quote": "expects to adopt the guidelines on high-risk systems by February 2027", "source": 1, "due": "2027-02-28"},
        {"claim": "Invented", "by": "Someone", "role": "", "quote": "words that are not in the source", "source": 1, "due": "2027-01-01"},
    ],
    "scorecard_hints": [{"id": "2026-10-26-1", "hint": "no evidence in this week's material"}],
    "review_notes": "",
}


class FakeClient:
    def __init__(self):
        self.calls = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **params):
        self.calls.append(params)
        return response(COLUMN, draft.WRITER_MODEL)


def article(slug, importance, primary=True):
    front = {
        "title": f"Story {slug}", "date": "2026-10-28", "dek": "Dek.", "whyItMatters": "Because.",
        "categories": ["ai-governance"], "whoShouldCare": ["CDO"], "importance": importance, "type": "Guidance",
        "deadlines": [{"date": date(2026, 11, 20), "what": f"Deadline for {slug}"}, {"date": date(2027, 6, 1), "what": "Far away"}],
        "sources": [{"name": "Blog", "title": "Coverage", "url": f"https://blog.example.org/{slug}"},
                    {"name": "European Commission", "title": "Press release", "url": f"https://ec.example.eu/{slug}", "primary": primary}],
    }
    return "---\n" + yaml.safe_dump(front) + "---\n\nBody of " + slug + ".\n"


class MondayTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        arts = self.tmp / "articles"
        arts.mkdir()
        (arts / "one.md").write_text(article("one", 4))
        (arts / "two.md").write_text(article("two", 2))
        (arts / "old.md").write_text(article("old", 5))
        (arts / "sample.md").write_text(article("sample", 5).replace("importance: 5", "importance: 5\nsample: true"))
        added = {"one": date(2026, 10, 27), "two": date(2026, 11, 1), "old": date(2026, 10, 20), "sample": date(2026, 10, 28)}
        (self.tmp / "predictions.yaml").write_text("# header\n" + yaml.safe_dump([
            {"id": "2026-10-26-1", "claim": "Old call", "by": "Data Governance Signal", "ours": True,
             "source": {"title": "c", "url": "https://x.org"}, "made": date(2026, 10, 26), "due": date(2026, 11, 5),
             "confidence": 60, "status": "open"},
            {"id": "2026-10-26-2", "claim": "Later", "by": "X", "quote": "q", "source": {"title": "c", "url": "https://x.org"},
             "made": date(2026, 10, 26), "due": date(2027, 5, 1), "status": "open"},
        ], sort_keys=False))
        self.client = FakeClient()
        self.fetched = []

        def fetch(url):
            self.fetched.append(url)
            return {"url": url, "text": SOURCE_TEXT, "links": []}

        self.patches = [
            mock.patch.object(monday, "ARTICLES", arts),
            mock.patch.object(monday, "COLUMNS", self.tmp / "columns"),
            mock.patch.object(monday, "PREDICTIONS", self.tmp / "predictions.yaml"),
            mock.patch.object(monday, "added_on", lambda p: added[p.stem]),
            mock.patch.object(draft, "fetch_source", fetch),
            mock.patch.object(draft, "STATE_PATH", self.tmp / "ai.json"),
            mock.patch.object(monday.anthropic, "Anthropic", lambda: self.client),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp)

    def run_monday(self, day=MONDAY):
        with mock.patch("builtins.print"):
            return monday.run(SimpleNamespace(date=day.isoformat(), no_pr=True))

    def test_package(self):
        summary = self.run_monday()
        self.assertEqual((summary["articles"], summary["predictions"], summary["dropped"], summary["due"]), (2, 2, 1, 1))
        # Only last week's real articles, most important first; primary sources fetched.
        prompt = self.client.calls[0]["messages"][0]["content"]
        self.assertLess(prompt.index("/news/one/"), prompt.index("/news/two/"))
        self.assertNotIn("/news/old/", prompt)
        self.assertNotIn("/news/sample/", prompt)
        self.assertEqual(self.fetched, ["https://ec.example.eu/one", "https://ec.example.eu/two"])

        col = (self.tmp / "columns" / "2026-11-02.md").read_text()
        front = yaml.safe_load(col.split("---")[1])
        self.assertEqual((front["title"], front["date"]), (COLUMN["title"], MONDAY))

        preds = yaml.safe_load((self.tmp / "predictions.yaml").read_text())
        self.assertTrue((self.tmp / "predictions.yaml").read_text().startswith("# header\n"))
        self.assertNotIn("&id", (self.tmp / "predictions.yaml").read_text())
        new = {p["id"]: p for p in preds[2:]}
        self.assertEqual(sorted(new), ["2026-11-02-1", "2026-11-02-2"])
        ours, theirs = new["2026-11-02-1"], new["2026-11-02-2"]
        self.assertEqual((ours["ours"], ours["confidence"], ours["due"]), (True, 65, date(2027, 6, 30)))
        self.assertEqual(ours["source"]["url"], "https://datagovernancesignal.com/monday-signal/2026-11-02/")
        self.assertEqual((theirs["by"], theirs["source"]["url"], theirs["status"]), ("European Commission", "https://ec.example.eu/one", "open"))
        self.assertNotIn("confidence", theirs)

        state = json.loads((self.tmp / "ai.json").read_text())
        self.assertGreater(state["usage"][draft.month_key()]["usd"], 0)

    def test_skips(self):
        self.assertIn("not a Monday", self.run_monday(date(2026, 11, 3))["skipped"])
        self.assertIn("no articles", self.run_monday(date(2026, 12, 7))["skipped"])
        self.run_monday()
        self.assertIn("already exists", self.run_monday()["skipped"])
        self.assertEqual(len(self.client.calls), 1)

    def test_pr_body_lists_due_and_newsletter(self):
        articles = monday.week_articles(MONDAY)
        due = monday.due_predictions(monday.load_predictions()[1], MONDAY)
        body = monday.pr_body(MONDAY, COLUMN, articles, [], [], due, COLUMN["scorecard_hints"])
        self.assertIn("`2026-10-26-1`", body)
        self.assertNotIn("2026-10-26-2", body)
        self.assertIn("https://datagovernancesignal.com/news/one/", body)
        self.assertIn("Monday 2 November 2026", body)

    def test_newsletter_sections(self):
        articles = monday.week_articles(MONDAY)
        preds = monday.load_predictions()[1]
        text = monday.newsletter_text(MONDAY, COLUMN, articles, monday.upcoming_dates(MONDAY), preds)
        for heading in ("## The Big Signal", "## Also this week", "## Governance in Practice", "## What to Watch",
                        "## One Practical Insight"):
            self.assertIn(heading, text)
        # The model's pick leads, even though "one" is more important.
        self.assertLess(text.index("/news/two/"), text.index("/news/one/"))
        watch = text[text.index("## What to Watch"):text.index("## One Practical Insight")]
        self.assertIn("**20 Nov** — Deadline for one", watch)
        self.assertNotIn("Far away", watch)
        self.assertIn("Deadline for old", watch)  # any published article's upcoming dates count
        self.assertNotIn("Deadline for sample", watch)
        self.assertIn("Prediction due: Old call", watch)
        self.assertNotIn("Later", watch)


class QuoteTest(unittest.TestCase):
    def test_quotes_match_despite_typography(self):
        sources = [{"ref": 1, "text": "He said: “We’ll  finish\nby May.”"}]
        kept, dropped = monday.verified_others(
            [{"quote": "\"We'll finish by May.\"", "source": 1}, {"quote": "We will finish", "source": 1}, {"quote": "May", "source": 2}],
            sources)
        self.assertEqual((len(kept), len(dropped)), (1, 2))


if __name__ == "__main__":
    unittest.main()
