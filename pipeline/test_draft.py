import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import yaml

import draft


def response(payload: dict, model: str, stop_reason: str = "end_turn"):
    return SimpleNamespace(
        model=model,
        stop_reason=stop_reason,
        stop_details=None,
        usage=SimpleNamespace(input_tokens=2000, output_tokens=500, cache_creation_input_tokens=0, cache_read_input_tokens=0),
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=json.dumps(payload))],
    )


DRAFT = {
    "title": "Regulator fines Example Corp EUR 2 million over unlawful profiling",
    "dek": "The decision finds the company relied on invalid consent for profiling customers.",
    "body": " ".join(["The regulator fined **Example Corp EUR 2 million** for profiling customers without valid consent."] * 4),
    "why_it_matters": "Consent records must show what each controller relied on.",
    "categories": ["privacy", "regulation", "privacy"],
    "institutions": ["garante", "edpb", "garante"],
    "who_should_care": ["DPO", "Legal & compliance"],
    "importance": 4,
    "type": "Enforcement",
    "region": "EU",
    "status_stage": "Decision",
    "status_detail": "may be appealed",
    "what_to_check": ["Check that consent records name each controller relying on them."],
    "deadlines": [{"date": "2026-12-01", "what": "Deadline to comply"}, {"date": "December 2026", "what": "vague"}],
    "card_figure": "EUR 2M",
    "card_caption": "Fine for profiling without valid consent",
    "editor_note": "",
    "sources": [
        {"ref": 1, "name": "Privacy Blog", "title": "Example Corp fined", "is_primary": False},
        {"ref": 2, "name": "Example DPA", "title": "Decision 12/2026", "is_primary": True},
    ],
    "related": [],
    "review_notes": "",
}


CHECK = {"claims": [
    {"claim": "Fine of EUR 2 million", "verdict": "supported", "source": 2, "evidence": "fine of EUR 2 000 000"},
    {"claim": "Company relied on invalid consent", "verdict": "partly", "source": 1, "evidence": "consent was not valid"},
]}


class FakeClient:
    def __init__(self, scores, primary_indices=(0,)):
        self.scores = scores
        self.primary_indices = list(primary_indices)
        self.writer_calls = 0
        self.check_calls = 0
        self.messages = SimpleNamespace(create=self._small)
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._large))

    def _small(self, **params):
        assert params["model"] == draft.SCORER_MODEL
        props = params["output_config"]["format"]["schema"]["properties"]
        if "items" in props:
            return response({"items": self.scores}, draft.SCORER_MODEL)
        payload = {"article_is_original": False, "primary_link_indices": self.primary_indices, "reason": "decision"}
        return response(payload, draft.SCORER_MODEL)

    def _large(self, **params):
        assert params["model"] == draft.WRITER_MODEL and params["fallbacks"] == "default"
        if "claims" in params["output_config"]["format"]["schema"]["properties"]:
            self.check_calls += 1
            return response(CHECK, draft.WRITER_MODEL)
        self.writer_calls += 1
        return response(DRAFT, draft.WRITER_MODEL)


def fake_fetch(url):
    if url == "https://dpa.example.org/decision.pdf":
        return {"url": url, "text": "decision text " * 200, "links": []}
    return {"url": url, "text": "news text " * 200,
            "links": [{"url": "https://dpa.example.org/decision.pdf", "text": "the decision"}]}


def item(i, **kw):
    base = {
        "id": f"id{i}", "source_id": "edpb", "source_name": "EDPB", "section": "core", "categories": ["privacy"],
        "priority": "high", "reliability": 3, "title": f"Item {i}", "url": f"https://example.org/{i}",
        "published": "2026-10-20T10:00:00Z", "first_seen": "2026-10-24T17:17:00Z", "excerpt": "", "method": "rss",
        "duplicate_of": None, "status": "new",
    }
    return {**base, **kw}


class RunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "archive").mkdir()
        (self.tmp / "state").mkdir()
        (self.tmp / "reports").mkdir()
        self.articles = self.tmp / "articles"
        self.articles.mkdir()
        shutil.copy(draft.ARTICLES / "edpb-guidelines-dsa-gdpr-interplay.md", self.articles)
        items = [item(0), item(1, title="Webinar"), item(2, duplicate_of="id0"), item(3, status="baseline")]
        (self.tmp / "archive" / "2026-10.jsonl").write_text("\n".join(json.dumps(i) for i in items) + "\n")
        self.patches = [
            mock.patch.object(draft, "DATA", self.tmp),
            mock.patch.object(draft, "ARTICLES", self.articles),
            mock.patch.object(draft, "STATE_PATH", self.tmp / "state" / "ai.json"),
            mock.patch.object(draft, "REPORT_PATH", self.tmp / "reports" / "drafts.md"),
            mock.patch.object(draft, "fetch_source", fake_fetch),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp)

    def run_with(self, scores):
        client = FakeClient(scores)
        with mock.patch.object(draft.anthropic, "Anthropic", lambda: client):
            summary = draft.run(SimpleNamespace(no_pr=True, score_only=False))
        return client, summary

    def test_full_run_writes_valid_draft_and_state(self):
        scores = [
            {"index": 0, "relevant": True, "importance": 4, "categories": ["privacy"], "same_story_as": "", "reason": "fine"},
            {"index": 1, "relevant": False, "importance": 1, "categories": [], "same_story_as": "", "reason": "webinar"},
        ]
        client, summary = self.run_with(scores)
        self.assertEqual((summary["scored"], summary["duplicates"], summary["drafted"]), (2, 1, 1))
        self.assertEqual((client.writer_calls, client.check_calls), (1, 1))

        path = self.articles / "regulator-fines-example-corp-eur-2-million-over-unlawful-profiling.md"
        front = yaml.safe_load(path.read_text().split("---")[1])
        self.assertEqual(front["categories"], ["privacy", "regulation"])  # de-duplicated
        self.assertEqual(front["institutions"], ["garante", "edpb"])
        # Primary source first, with the URL of the fetched original document.
        self.assertEqual(front["sources"][0]["primary"], True)
        self.assertEqual(front["sources"][0]["url"], "https://dpa.example.org/decision.pdf")
        self.assertEqual(front["sources"][1]["url"], "https://example.org/0")
        self.assertEqual(front["card"]["figure"], "EUR 2M")
        self.assertEqual(front["status"], {"stage": "Decision", "detail": "may be appealed"})
        self.assertEqual(len(front["whatToCheck"]), 1)
        self.assertEqual([str(x["date"]) for x in front["deadlines"]], ["2026-12-01"])  # vague date dropped
        self.assertEqual(str(front["date"]), "2026-10-20")

        state = json.loads((self.tmp / "state" / "ai.json").read_text())
        self.assertEqual(state["processed"]["id0"]["decision"], "drafted")
        self.assertEqual((state["processed"]["id0"]["primary_found"], state["processed"]["id0"]["flagged"]), (True, 1))
        self.assertEqual(state["processed"]["id1"]["decision"], "skipped")
        self.assertEqual(state["processed"]["id2"]["decision"], "duplicate")
        self.assertNotIn("id3", state["processed"])
        self.assertGreater(state["usage"][draft.month_key()]["usd"], 0)

        # A second run has nothing left to do and makes no API calls.
        client, summary = self.run_with([])
        self.assertEqual((summary["candidates"], client.writer_calls), (0, 0))

    def test_budget_stops_drafting_and_keeps_queue(self):
        draft.save_state({"processed": {}, "usage": {draft.month_key(): {"usd": 0.0, "calls": 0}}})
        scores = [{"index": 0, "relevant": True, "importance": 5, "categories": ["regulation"], "same_story_as": "", "reason": "x"}]
        with mock.patch.object(draft, "MONTHLY_BUDGET_USD", 0.0001):
            client, summary = self.run_with(scores)
        self.assertTrue(summary["budget_stop"])
        self.assertEqual(client.writer_calls, 0)


class RulesTest(unittest.TestCase):
    cats = [{"id": "privacy", "section": "core"}, {"id": "platforms", "section": "broad"}]

    def test_thresholds(self):
        s = lambda imp, cats, rel=True, same="": {"relevant": rel, "importance": imp, "categories": cats, "same_story_as": same}
        self.assertTrue(draft.should_draft(s(3, ["privacy"]), self.cats))
        self.assertFalse(draft.should_draft(s(3, ["platforms"]), self.cats))
        self.assertTrue(draft.should_draft(s(4, ["platforms"]), self.cats))
        self.assertFalse(draft.should_draft(s(5, ["privacy"], rel=False), self.cats))
        self.assertFalse(draft.should_draft(s(5, ["privacy"], same="x"), self.cats))

    def test_validate_flags_long_card(self):
        self.assertIn("card_figure longer than 22 characters", draft.validate({**DRAFT, "card_figure": "x" * 30}))
        self.assertEqual(draft.validate(DRAFT), [])

    def test_status_stages_read_from_site(self):
        stages = draft.status_vocabulary()
        self.assertIn("In negotiation", stages)
        self.assertIn("Unconfirmed", stages)
        self.assertEqual(len(stages), 15)

    def test_what_to_check_only_for_important_items(self):
        d = draft.tidy({**DRAFT, "importance": 3, "deadlines": [], "what_to_check": ["x"]})
        self.assertEqual(d["what_to_check"], [])

    def test_institutions_read_from_site(self):
        ids = [i["id"] for i in draft.institution_vocabulary()]
        self.assertIn("edpb", ids)
        self.assertIn("cjeu", ids)

    def test_unique_slug(self):
        self.assertEqual(draft.unique_slug("A b", {"a-b"}), "a-b-2")


if __name__ == "__main__":
    unittest.main()


class CheckSummaryTest(unittest.TestCase):
    def test_summary_lists_flagged_claims(self):
        self.assertIn("all 3 claims", draft.check_summary({"claims": 3, "flagged": []}))
        text = draft.check_summary({"claims": 2, "flagged": [CHECK["claims"][1]]})
        self.assertIn("1 of 2 claims", text)
        self.assertIn("Company relied on invalid consent", text)


class ExtractLinksTest(unittest.TestCase):
    def test_skips_social_and_short_links(self):
        html = (
            '<a href="/decisions/12.pdf">Read the decision</a><a href="https://x.com/dpa">X</a>'
            '<a href="https://twitter.com/dpa">Follow us on Twitter</a><a href="#top">Back to top</a>'
            '<a href="mailto:a@b.c">Email us</a>'
        )
        links = draft.extract_links(html, "https://dpa.example.org/news/fine")
        self.assertEqual(links, [{"url": "https://dpa.example.org/decisions/12.pdf", "text": "Read the decision"}])


class FactCheckThresholdTest(RunTest):
    def test_low_importance_draft_is_not_fact_checked(self):
        scores = [{"index": 0, "relevant": True, "importance": 3, "categories": ["privacy"], "same_story_as": "", "reason": "x"}]
        with mock.patch.dict(DRAFT, importance=3):
            client, summary = self.run_with(scores)
        self.assertEqual((summary["drafted"], client.writer_calls, client.check_calls), (1, 1, 0))
        self.assertIn("not run", draft.check_summary({"claims": 0, "flagged": [], "skipped": True}))


class SameStoryTest(RunTest):
    def test_same_story_in_one_batch_is_drafted_once(self):
        scores = [
            {"index": 0, "relevant": True, "importance": 4, "categories": ["privacy"], "same_story_as": "", "same_as_index": -1, "reason": "x"},
            {"index": 1, "relevant": True, "importance": 4, "categories": ["privacy"], "same_story_as": "", "same_as_index": 0, "reason": "same launch"},
        ]
        client, summary = self.run_with(scores)
        self.assertEqual((summary["selected"], summary["drafted"], client.writer_calls), (1, 1, 1))
        state = json.loads((self.tmp / "state" / "ai.json").read_text())
        self.assertEqual(state["processed"]["id1"]["decision"], "skipped")
        self.assertEqual(state["processed"]["id1"]["same_story_as"], "item:id0")

    def test_pending_draft_titles_are_cleaned(self):
        out = json.dumps([{"title": "⚠️ Draft: Monte Carlo launches Bayes — Importance 3", "headRefName": "drafts/monte-carlo-bayes"},
                          {"title": "Monday Signal 2026-11-02: x", "headRefName": "columns/2026-11-02"}])
        with mock.patch.object(draft.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=out)):
            self.assertEqual(draft.pending_drafts(), [{"slug": "monte-carlo-bayes", "title": "Monte Carlo launches Bayes", "date": ""}])
