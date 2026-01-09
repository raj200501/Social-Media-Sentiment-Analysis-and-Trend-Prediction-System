"""Load sentiment calibration from disk."""
from __future__ import annotations

import json
from pathlib import Path

from sentiment_analysis.model_training import SentimentCalibration

DEFAULT_MODEL_PATH = Path("models/sentiment_calibration.json")


def load_model(path: Path = DEFAULT_MODEL_PATH) -> SentimentCalibration:
    if not path.exists():
        raise FileNotFoundError(
            f"Sentiment calibration not found at {path}. Run models/save_model.py first."
        )
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return SentimentCalibration(**payload)


if __name__ == "__main__":
    calibration = load_model()
    print("Sentiment calibration loaded:")
    print(calibration)
