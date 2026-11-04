import json
import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

import social


def story(folder: Path, name: str, **front):
    folder.mkdir(parents=True, exist_ok=True)
    lines = ["---"] + [f"{k}: {json.dumps(v)}" for k, v in front.items()] + ["---", "", "Body."]
    (folder / f"{name}.md").write_text("\n".join(lines) + "\n")


class SocialTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.content = self.tmp / "content"
        story(self.content / "articles", "old-story", title="Old story", date="2026-11-01", dek="Old.", categories=["privacy"])
        story(self.content / "opinion", "essay", title="An essay", date="2026-11-10", dek="Later.")
        (self.content / "columns").mkdir()
        self.patches = [
            mock.patch.object(social, "CONTENT", self.content),
            mock.patch.object(social, "STATE_PATH", self.tmp / "social.json"),
            mock.patch.object(social, "wait_until_live", lambda url, s: True),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp)

    def state(self):
        return json.loads((self.tmp / "social.json").read_text())

    def test_first_run_records_without_posting(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            self.assertEqual(social.run(date(2026, 11, 4)), {"baseline": 1, "posted": 0})
        self.assertIn("news/old-story", self.state()["posted"])
        self.assertNotIn("opinion/essay", self.state()["posted"])  # not published yet

    def test_new_story_posted_once_to_each_account(self):
        social.run(date(2026, 11, 4))
        story(self.content / "articles", "new-story", title="CNIL fines Example", date="2026-11-04",
              dek="The regulator says consent was not valid.", categories=["privacy", "regulation"])
        sent = []
        accounts = {"bluesky": lambda i: sent.append(("b", i["key"])) or "at://x",
                    "mastodon": lambda i: sent.append(("m", i["key"])) or "https://m/1"}
        with mock.patch.object(social, "platforms", lambda: accounts):
            self.assertEqual(social.run(date(2026, 11, 4))["posted"], 1)
            self.assertEqual(social.run(date(2026, 11, 4))["posted"], 0)  # not twice
            # The essay is posted on its publication day.
            self.assertEqual(social.run(date(2026, 11, 10))["posted"], 1)
        self.assertEqual(sent, [("b", "news/new-story"), ("m", "news/new-story"), ("b", "opinion/essay"), ("m", "opinion/essay")])
        self.assertEqual(self.state()["posted"]["news/new-story"]["mastodon"], "https://m/1")

    def test_without_accounts_new_stories_are_skipped_not_queued(self):
        social.run(date(2026, 11, 4))
        story(self.content / "articles", "new-story", title="T", date="2026-11-04", dek="D")
        with mock.patch.object(social, "platforms", lambda: {}):
            self.assertEqual(social.run(date(2026, 11, 4))["skipped"], 1)
        self.assertIn("skipped", self.state()["posted"]["news/new-story"])

    def test_failed_post_is_retried(self):
        social.run(date(2026, 11, 4))
        story(self.content / "articles", "new-story", title="T", date="2026-11-04", dek="D")
        def broken(item):
            raise social.requests.HTTPError("401 Unauthorized")
        with mock.patch.object(social, "platforms", lambda: {"bluesky": broken}):
            self.assertEqual(social.run(date(2026, 11, 4))["failed"], 1)
        self.assertNotIn("news/new-story", self.state()["posted"])

    def test_texts_fit_the_platform_limits(self):
        item = {"key": "news/x", "kind": "news", "url": "https://datagovernancesignal.com/news/" + "x" * 70 + "/",
                "title": "T" * 110, "dek": "word " * 80, "categories": ["privacy", "ai-governance", "regulation"]}
        self.assertLessEqual(len(social.bluesky_text(item)), 300)
        text = social.mastodon_text(item)
        self.assertLessEqual(len(text) - len(item["url"]) + 23, 500)
        self.assertIn("#DataGovernance #Privacy #AIGovernance", text)
        self.assertTrue(social.mastodon_text({**item, "kind": "opinion"}).startswith("Editor's Opinion: "))


if __name__ == "__main__":
    unittest.main()
