"""Load social media data from a CSV file."""
from __future__ import annotations

from pathlib import Path
import csv

DEFAULT_DATA_PATH = Path("data/sample_data.csv")


def load_data(file_path: str | Path = DEFAULT_DATA_PATH) -> list[dict[str, str]]:
    """Load raw social media data.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A list of dictionaries with the raw data.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(
            f"Expected data file at {file_path}. Run scripts/generate_sample_data.py first."
        )
    with file_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


if __name__ == "__main__":
    data = load_data()
    print(data[:5])
