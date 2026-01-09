import unittest

from api.api_server import load_dataset, sentiment_series


class TestAPIHelpers(unittest.TestCase):
    def test_sentiment_series_has_data(self):
        data = load_dataset()
        series = sentiment_series(data)
        self.assertGreater(len(series), 0)
        self.assertIn("date", series[0])
        self.assertIn("score", series[0])


if __name__ == "__main__":
    unittest.main()
