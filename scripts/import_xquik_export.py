"""Command-line importer for Xquik tweet exports."""
from __future__ import annotations

from pathlib import Path
import argparse

from data.xquik_import import DEFAULT_OUTPUT_PATH, import_xquik_export


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a Xquik CSV, JSON, or JSONL tweet export into sample_data.csv."
    )
    parser.add_argument("input", help="Path to the Xquik export file.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output CSV path. Defaults to data/sample_data.csv.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = import_xquik_export(Path(args.input), Path(args.output))
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
