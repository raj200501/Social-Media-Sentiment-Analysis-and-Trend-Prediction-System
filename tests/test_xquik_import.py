import csv
import json
import tempfile
import unittest
from pathlib import Path

from data.xquik_import import import_xquik_export, normalize_xquik_rows, read_xquik_rows


class TestXquikImport(unittest.TestCase):
    def test_normalize_xquik_rows_maps_export_fields(self):
        rows = normalize_xquik_rows(
            [
                {
                    "tweet_id": "tweet-1",
                    "created_at": "2024-02-03T12:30:00Z",
                    "full_text": "Great launch #ai",
                    "like_count": "12",
                    "retweet_count": "4",
                },
                {
                    "tweet_id": "tweet-1",
                    "created_at": "2024-02-03T12:30:00Z",
                    "full_text": "Duplicate row",
                },
                {"tweet_id": "tweet-2", "full_text": "   "},
            ]
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "tweet-1")
        self.assertEqual(rows[0]["created_at"], "2024-02-03")
        self.assertEqual(rows[0]["platform"], "x")
        self.assertEqual(rows[0]["content"], "Great launch #ai")
        self.assertEqual(rows[0]["likes"], 12)
        self.assertEqual(rows[0]["shares"], 4)

    def test_import_xquik_export_writes_sample_schema_from_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "xquik.jsonl"
            output_path = Path(tmp_dir) / "sample_data.csv"
            rows = [
                {"id": "1", "text": "Love the release", "likes": 3, "shares": 2},
                {"id": "2", "text": "Monitoring the launch", "likes": 0, "shares": 1},
            ]
            input_path.write_text(
                "\n".join(json.dumps(row) for row in rows),
                encoding="utf-8",
            )

            imported = import_xquik_export(input_path, output_path)

            self.assertEqual(len(imported), 2)
            with output_path.open("r", newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                written = list(reader)
            self.assertEqual(reader.fieldnames, ["id", "created_at", "platform", "content", "likes", "shares"])
            self.assertEqual(written[0]["platform"], "x")
            self.assertEqual(written[0]["content"], "Love the release")

    def test_read_xquik_rows_accepts_wrapped_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "wrapped.json"
            input_path.write_text(
                json.dumps({"tweets": [{"id": "wrapped-1", "text": "Wrapped export"}]}),
                encoding="utf-8",
            )

            rows = read_xquik_rows(input_path)

            self.assertEqual(rows, [{"id": "wrapped-1", "text": "Wrapped export"}])


if __name__ == "__main__":
    unittest.main()
