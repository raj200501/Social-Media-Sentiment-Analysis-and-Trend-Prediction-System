import unittest

from trend_detection.trend_detection import build_trend_timeseries, detect_trends


def sample_data():
    return [
        {
            "id": "1",
            "created_at": "2024-01-01",
            "platform": "twitter",
            "content": "Love the #ai release",
        },
        {
            "id": "2",
            "created_at": "2024-01-02",
            "platform": "reddit",
            "content": "#ai continues to impress",
        },
        {
            "id": "3",
            "created_at": "2024-01-02",
            "platform": "reddit",
            "content": "Exploring #opensource tools",
        },
    ]


class TestTrendDetection(unittest.TestCase):
    def test_detect_trends_returns_top_term(self):
        trends = detect_trends(sample_data(), top_n=2, min_count=1)
        self.assertIn("#ai", trends)

    def test_build_trend_timeseries_counts_mentions(self):
        series = build_trend_timeseries(sample_data(), "#ai")
        counts = [point["count"] for point in series]
        self.assertEqual(sum(counts), 2)


if __name__ == "__main__":
    unittest.main()
