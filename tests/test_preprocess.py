import csv
import json
import tempfile
import unittest
from pathlib import Path

from data.preprocess_data import normalize_text, preprocess_data, tokenize


class TestPreprocess(unittest.TestCase):
    def test_normalize_text_removes_noise(self):
        raw = "Hello!!!  This is a Test."
        self.assertEqual(normalize_text(raw), "hello this is a test")

    def test_tokenize_extracts_words(self):
        tokens = tokenize("Love #ai and clean code!")
        self.assertIn("love", tokens)
        self.assertIn("#ai", tokens)

    def test_preprocess_data_creates_output(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "sample.csv"
            output_path = Path(tmp_dir) / "processed.csv"
            with input_path.open("w", newline="", encoding="utf-8") as handle:
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
                        "content": "Love the #ai update!",
                        "likes": 10,
                        "shares": 2,
                    }
                )

            processed = preprocess_data(input_path=input_path, output_path=output_path)

            self.assertTrue(output_path.exists())
            self.assertIn("cleaned_content", processed[0])
            self.assertIn("tokens", processed[0])
            tokens = json.loads(processed[0]["tokens"])
            self.assertIn("#ai", tokens)


if __name__ == "__main__":
    unittest.main()
