"""Preprocess raw social media data and create a cleaned dataset."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import csv
import json
import re
from typing import Iterable

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_PATH = ROOT_DIR / "data" / "sample_data.csv"
DEFAULT_OUTPUT_PATH = ROOT_DIR / "data" / "processed_data.csv"

WORD_PATTERN = re.compile(r"#\w+|\b\w+\b")


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s#]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def tokenize(text: str) -> list[str]:
    return WORD_PATTERN.findall(normalize_text(text))


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return rows


def _write_csv(path: Path, rows: Iterable[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def preprocess_data(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> list[dict[str, str]]:
    """Load raw data, clean text, and write processed data.

    Args:
        input_path: Path to the raw CSV file.
        output_path: Path to write the processed CSV file.

    Returns:
        List of processed rows as dictionaries.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Expected input data at {input_path}. Run scripts/generate_sample_data.py first."
        )

    rows = _read_csv(input_path)
    if not rows:
        raise ValueError("Input dataset is empty")

    required_columns = {"id", "created_at", "platform", "content"}
    missing = required_columns - set(rows[0].keys())
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    processed_rows = []
    for row in rows:
        try:
            datetime.fromisoformat(row["created_at"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Invalid dates detected in created_at column") from exc

        cleaned = normalize_text(row["content"])
        tokens = tokenize(row["content"])

        updated = dict(row)
        updated["cleaned_content"] = cleaned
        updated["tokens"] = json.dumps(tokens)
        processed_rows.append(updated)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(processed_rows[0].keys())
    _write_csv(output_path, processed_rows, fieldnames)
    return processed_rows


if __name__ == "__main__":
    preprocess_data()
    print("Data preprocessing complete")
