"""Train a lightweight baseline sentiment model.

This module doesn't train a statistical model; instead, it computes summary
statistics over the labeled data to calibrate threshold ranges. It keeps the
workflow reproducible without heavy ML dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv

from sentiment_analysis.sentiment import analyze_sentiment


@dataclass(frozen=True)
class SentimentCalibration:
    positive_threshold: float
    negative_threshold: float
    average_score: float


def _read_content(input_path: Path) -> list[str]:
    with input_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [row["content"] for row in reader]


def train_sentiment_baseline(
    input_path: str | Path = Path("data/processed_data.csv"),
) -> SentimentCalibration:
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Processed data not found at {input_path}. Run data/preprocess_data.py first."
        )

    contents = _read_content(input_path)
    if not contents:
        raise ValueError("Processed dataset is empty")

    scores = [analyze_sentiment(text).score for text in contents]
    average_score = sum(scores) / len(scores)

    positive_threshold = max(0.15, average_score + 0.05)
    negative_threshold = min(-0.15, average_score - 0.05)

    return SentimentCalibration(
        positive_threshold=round(positive_threshold, 3),
        negative_threshold=round(negative_threshold, 3),
        average_score=round(average_score, 3),
    )


def main() -> None:
    calibration = train_sentiment_baseline()
    print("Sentiment baseline trained:")
    print(calibration)


if __name__ == "__main__":
    main()
