"""Persist sentiment calibration to disk."""
from __future__ import annotations

import json
from pathlib import Path

from sentiment_analysis.model_training import train_sentiment_baseline

DEFAULT_MODEL_PATH = Path("models/sentiment_calibration.json")


def save_model(path: Path = DEFAULT_MODEL_PATH) -> Path:
    calibration = train_sentiment_baseline()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(calibration.__dict__, handle, indent=2)
    return path


if __name__ == "__main__":
    output_path = save_model()
    print(f"Sentiment calibration saved to {output_path}")
