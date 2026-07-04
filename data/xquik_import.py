"""Normalize Xquik tweet exports into this project's raw data schema."""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable
import csv
import json

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_PATH = ROOT_DIR / "data" / "sample_data.csv"

FIELDNAMES = ["id", "created_at", "platform", "content", "likes", "shares"]
TEXT_FIELDS = ("text", "content", "full_text", "tweet_text", "Tweet_Text")
DATE_FIELDS = ("created_at", "createdAt", "date", "timestamp")
LIKE_FIELDS = ("likes", "like_count", "favorite_count", "favorites")
SHARE_FIELDS = ("shares", "retweet_count", "reposts", "retweets")
ID_FIELDS = ("id", "tweet_id", "Tweet_ID", "url")
WRAPPED_FIELDS = ("tweets", "data", "results", "items")


def _first_value(row: dict[str, Any], fields: Iterable[str]) -> Any:
    for field in fields:
        value = row.get(field)
        if value not in (None, ""):
            return value
    return None


def _coerce_date(value: Any) -> str:
    if value in (None, ""):
        return date.today().isoformat()
    raw = str(value).strip()
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return raw[:10]


def _coerce_int(value: Any) -> int:
    if value in (None, ""):
        return 0
    try:
        return max(0, int(float(str(value).replace(",", ""))))
    except ValueError:
        return 0


def _read_json_rows(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    stripped = text.strip()
    if not stripped:
        return []
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in stripped.splitlines() if line.strip()]

    payload = json.loads(stripped)
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for field in WRAPPED_FIELDS:
            rows = payload.get(field)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []


def _read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_xquik_rows(path: str | Path) -> list[dict[str, Any]]:
    """Read a Xquik CSV, JSON, or JSONL export."""
    input_path = Path(path)
    suffix = input_path.suffix.lower()
    if suffix in {".json", ".jsonl"}:
        return _read_json_rows(input_path)
    return _read_csv_rows(input_path)


def normalize_xquik_rows(rows: Iterable[dict[str, Any]]) -> list[dict[str, str | int]]:
    """Map exported tweet rows into the raw project dataset schema."""
    normalized = []
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        content = _first_value(row, TEXT_FIELDS)
        if content is None or not str(content).strip():
            continue

        row_id = _first_value(row, ID_FIELDS) or f"xquik-{index}"
        key = str(row_id)
        if key in seen:
            continue
        seen.add(key)

        normalized.append(
            {
                "id": key,
                "created_at": _coerce_date(_first_value(row, DATE_FIELDS)),
                "platform": "x",
                "content": str(content).strip(),
                "likes": _coerce_int(_first_value(row, LIKE_FIELDS)),
                "shares": _coerce_int(_first_value(row, SHARE_FIELDS)),
            }
        )
    return normalized


def write_sample_data(rows: Iterable[dict[str, str | int]], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def import_xquik_export(
    input_path: str | Path,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> list[dict[str, str | int]]:
    """Convert a Xquik export into data/sample_data.csv rows."""
    rows = normalize_xquik_rows(read_xquik_rows(input_path))
    if not rows:
        raise ValueError("No tweet text rows found in the Xquik export.")
    write_sample_data(rows, output_path)
    return rows
