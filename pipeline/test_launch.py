import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import launch

SITE = "export const SITE = {\n  name: 'X',\n  preview: true,\n  launchAt: '2026-10-30T11:00:00Z',\n};\n"


def article(sample: bool) -> str:
    return "---\ntitle: T\n" + ("sample: true\n" if sample else "") + "---\n\nBody.\n"


class LaunchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "articles").mkdir()
        (self.tmp / "site.ts").write_text(SITE)
        (self.tmp / "articles" / "real.md").write_text(article(False))
        (self.tmp / "articles" / "sample.md").write_text(article(True))
        self.patches = [mock.patch.object(launch, "SITE_TS", self.tmp / "site.ts"),
                        mock.patch.object(launch, "ARTICLES", self.tmp / "articles")]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp)

    def at(self, minutes_before: float):
        return lambda: datetime(2026, 10, 30, 11, tzinfo=timezone.utc) - timedelta(minutes=minutes_before)

    def test_waits_until_a_minute_before_launch_then_launches_once(self):
        slept = []
        result = launch.run(False, sleep=slept.append, clock=self.at(5))
        self.assertEqual(slept, [240.0])
        self.assertIn("1 sample articles removed", result)
        self.assertIn("preview: false,", (self.tmp / "site.ts").read_text())
        self.assertEqual(sorted(p.name for p in (self.tmp / "articles").iterdir()), ["real.md"])
        self.assertEqual(launch.run(False, sleep=slept.append, clock=self.at(5)), "already live")

    def test_refuses_on_the_wrong_day(self):
        with self.assertRaises(SystemExit):
            launch.run(False, sleep=lambda s: None, clock=self.at(60 * 24))
        self.assertIn("preview: true,", (self.tmp / "site.ts").read_text())

    def test_late_start_launches_immediately(self):
        slept = []
        launch.run(False, sleep=slept.append, clock=self.at(-30))
        self.assertEqual(slept, [])

    def test_real_site_file_has_the_flags(self):
        ts = Path(launch.ROOT / "src" / "data" / "site.ts").read_text()
        self.assertEqual(launch.launch_at(ts), datetime(2026, 10, 30, 11, tzinfo=timezone.utc))


if __name__ == "__main__":
    unittest.main()
