import unittest

from ingest import canonical_url, item_id, jaccard, keyword_regex, title_tokens


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


if __name__ == "__main__":
    unittest.main()
