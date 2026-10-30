import os
import unittest
from datetime import date
from types import SimpleNamespace
from unittest import mock

import metrics


def reply(data):
    return SimpleNamespace(raise_for_status=lambda: None, json=lambda: {"data": {"viewer": {"accounts": [data]}}})


SITES = {"rumPageloadEventsAdaptiveGroups": [
    {"count": 3, "dimensions": {"siteTag": "other", "requestHost": "example.org"}},
    {"count": 40, "dimensions": {"siteTag": "abc123", "requestHost": "datagovernancesignal.com"}},
]}
STATS = {
    "total": [{"count": 50, "sum": {"visits": 40}}],
    "days": [{"count": 20, "sum": {"visits": 15}, "dimensions": {"date": "2026-10-29"}},
             {"count": 30, "sum": {"visits": 25}, "dimensions": {"date": "2026-10-30"}}],
    "pages": [{"count": 12, "dimensions": {"requestPath": "/"}}],
    "countries": [{"count": 30, "dimensions": {"countryName": "HR"}}],
    "referrers": [{"count": 5, "dimensions": {"refererHost": ""}}],
}


class WebAnalyticsTest(unittest.TestCase):
    def test_finds_site_tag_and_summarises(self):
        calls = []

        def post(url, json, headers, timeout):
            calls.append(json)
            return reply(SITES if "siteTag requestHost" in json["query"] else STATS)

        env = {"CF_API_TOKEN": "t", "CF_ACCOUNT_ID": "acc"}
        with mock.patch.dict(os.environ, env, clear=False), mock.patch.object(metrics.requests, "post", post):
            os.environ.pop("CF_SITE_TAG", None)
            web = metrics.web_analytics(date(2026, 10, 1), date(2026, 10, 30))
        self.assertEqual(calls[1]["variables"]["filter"]["siteTag"], "abc123")
        self.assertEqual((web["visits"], web["page_views"], len(web["by_day"])), (40, 50, 2))
        self.assertEqual(web["referrers"], [{"refererHost": "(direct)", "page_views": 5}])
        report = metrics.traffic_report({"month": "2026-10", "updated": "now", "web": web, "feedback": None})
        self.assertIn("**40 visits · 50 page views** this month (bots excluded)", report)
        self.assertEqual(calls[1]["variables"]["filter"]["bot"], 0)
        self.assertIn("| 2026-10-30 | 25 | 30 |", report)

    def test_graphql_error_is_recorded(self):
        bad = SimpleNamespace(raise_for_status=lambda: None, json=lambda: {"errors": [{"message": "not authorized"}]})
        with mock.patch.dict(os.environ, {"CF_API_TOKEN": "t", "CF_ACCOUNT_ID": "a", "CF_SITE_TAG": "s"}), \
                mock.patch.object(metrics.requests, "post", lambda *a, **k: bad):
            self.assertEqual(metrics.web_analytics(date(2026, 10, 1), date(2026, 10, 30)), {"error": "not authorized"})

    def test_not_configured(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(metrics.web_analytics(date(2026, 10, 1), date(2026, 10, 30)))


if __name__ == "__main__":
    unittest.main()
