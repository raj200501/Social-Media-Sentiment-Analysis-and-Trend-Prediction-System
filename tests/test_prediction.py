import csv
import tempfile
import unittest
from pathlib import Path

from trend_prediction.prediction import predict_trend_counts, predict_trend


class TestPrediction(unittest.TestCase):
    def test_predict_trend_counts_length(self):
        history = [
            {"date": "2024-01-01", "count": 1},
            {"date": "2024-01-02", "count": 2},
            {"date": "2024-01-03", "count": 3},
        ]
        forecast = predict_trend_counts(history, horizon=5)
        self.assertEqual(len(forecast), 5)

    def test_predict_trend_from_dataset(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "data.csv"
            output_path = Path(tmp_dir) / "processed.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["id", "created_at", "platform", "content", "likes", "shares"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "id": 1,
                        "created_at": "2024-01-01",
                        "platform": "twitter",
                        "content": "Love the #ai release",
                        "likes": 1,
                        "shares": 1,
                    }
                )
                writer.writerow(
                    {
                        "id": 2,
                        "created_at": "2024-01-02",
                        "platform": "reddit",
                        "content": "#ai continues to impress",
                        "likes": 1,
                        "shares": 1,
                    }
                )

            forecast = predict_trend("#ai", data_path=path, output_path=output_path, horizon=3)
            self.assertEqual(forecast.term, "#ai")
            self.assertEqual(len(forecast.forecast), 3)


if __name__ == "__main__":
    unittest.main()
