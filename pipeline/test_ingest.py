import unittest

from ingest import canonical_url, item_id, jaccard, keyword_regex, scrape_page, title_tokens


class CanonicalUrlTest(unittest.TestCase):
    def test_tracking_params_www_and_slash_removed(self):
        a = "https://www.example.com/news/item/?utm_source=x&utm_medium=rss&id=7#top"
        b = "http://example.com/news/item?id=7"
        self.assertEqual(canonical_url(a), canonical_url(b))
        self.assertEqual(item_id(a), item_id(b))

    def test_meaningful_query_kept(self):
        self.assertNotEqual(item_id("https://a.org/p?id=1"), item_id("https://a.org/p?id=2"))


class DuplicateTest(unittest.TestCase):
    def test_same_story_different_outlets(self):
        a = title_tokens("Norwegian DPA fines Xandr NOK 92 million for unlawful processing")
        b = title_tokens("Norwegian DPA fines Xandr NOK 92 million over unlawful processing of data")
        self.assertGreaterEqual(jaccard(a, b), 0.7)

    def test_different_stories(self):
        a = title_tokens("Italian DPA fines IQVIA EUR 7 million")
        b = title_tokens("EDPB adopts guidelines on DSA and GDPR interplay")
        self.assertLess(jaccard(a, b), 0.3)


class KeywordTest(unittest.TestCase):
    def test_word_boundaries(self):
        kw = keyword_regex(["fine", "AI Act", "GDPR"])
        self.assertTrue(kw.search("Regulator issues fine under GDPR"))
        self.assertTrue(kw.search("New guidance on the AI Act"))
        self.assertFalse(kw.search("Finance ministry defines budget"))


class ScrapeTest(unittest.TestCase):
    PAGE = """<meta charset="utf-8"><div class="item"><a href="upload/cp1en.pdf">Judgment of the Court in Case C-1/26 Example</a>
    <p>Data protection: the controller must explain the logic of automated decisions</p>
    <a href="upload/cp1de.pdf">DE</a></div><a href="/about">About the Court of Justice</a>"""

    def test_rewrite_item_summary_and_charset(self):
        rules = {"link_pattern": r"^https://c\.eu/site/upload/cp\d+en\.pdf$", "item": ".item",
                 "rewrite": {"from": r"^https://c\.eu/site/jcms/x/en/upload/", "to": "https://c.eu/site/upload/"}}
        found = scrape_page(self.PAGE.encode(), "https://c.eu/site/jcms/x/en/", rules)
        self.assertEqual([c.url for c in found], ["https://c.eu/site/upload/cp1en.pdf"])
        self.assertIn("automated decisions", found[0].summary)
        page = '<meta charset="utf-8"><a href="/n/1">Speaker\u2019s Office appoints a new board member</a>'
        self.assertEqual(scrape_page(page.encode(), "https://c.eu/", {"link_pattern": "/n/"})[0].title,
                         "Speaker\u2019s Office appoints a new board member")

    def test_link_limit(self):
        page = "".join(f'<a href="/n/{i}">Announcement number {i} of the agency</a>' for i in range(100))
        self.assertEqual(len(scrape_page(page.encode(), "https://c.eu/", {"link_pattern": "/n/"})), 40)


if __name__ == "__main__":
    unittest.main()
