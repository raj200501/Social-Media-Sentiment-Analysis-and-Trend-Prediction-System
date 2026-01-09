import unittest

from sentiment_analysis.sentiment import analyze_sentiment, score_tokens


class TestSentiment(unittest.TestCase):
    def test_analyze_sentiment_positive(self):
        result = analyze_sentiment("I love the fantastic update")
        self.assertEqual(result.label, "positive")
        self.assertGreater(result.score, 0)

    def test_analyze_sentiment_negative(self):
        result = analyze_sentiment("The outage was terrible and frustrating")
        self.assertEqual(result.label, "negative")
        self.assertLess(result.score, 0)

    def test_score_tokens_neutral(self):
        result = score_tokens(["release", "notes", "shared"])
        self.assertEqual(result.label, "neutral")
        self.assertEqual(result.score, 0)


if __name__ == "__main__":
    unittest.main()
