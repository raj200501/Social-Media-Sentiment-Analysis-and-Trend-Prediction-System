"""Compatibility module for sentiment preprocessing."""
from __future__ import annotations

from pathlib import Path

from data.preprocess_data import normalize_text, preprocess_data, tokenize

__all__ = ["normalize_text", "tokenize", "preprocess_data", "preprocess_sentiment_data"]


def preprocess_sentiment_data(
    input_path: str | Path = Path("data/sample_data.csv"),
    output_path: str | Path = Path("data/processed_data.csv"),
) -> list[dict[str, str]]:
    """Alias for preprocess_data to keep sentiment pipeline consistent."""
    return preprocess_data(input_path=input_path, output_path=output_path)


if __name__ == "__main__":
    preprocess_sentiment_data()
    print("Sentiment data preprocessing complete")
