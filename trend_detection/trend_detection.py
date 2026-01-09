"""Detect emerging trends from social media posts."""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable

from data.preprocess_data import tokenize


@dataclass(frozen=True)
class TrendResult:
    term: str
    series: list[dict[str, int | str]]


STOP_WORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "on",
    "for",
    "with",
    "in",
    "of",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "am",
    "it",
    "this",
    "that",
    "we",
    "you",
    "they",
    "i",
    "our",
    "your",
    "their",
    "from",
}


def extract_terms(texts: Iterable[str]) -> list[str]:
    terms: list[str] = []
    for text in texts:
        tokens = tokenize(text)
        for token in tokens:
            if token.startswith("#") or token not in STOP_WORDS:
                terms.append(token)
    return terms


def detect_trends(data: list[dict[str, str]], top_n: int = 5, min_count: int = 10) -> list[str]:
    terms = extract_terms(row["content"] for row in data)
    counts = Counter(terms)
    ranked = [term for term, count in counts.most_common() if count >= min_count]
    return ranked[:top_n]


def _date_range(start: datetime, end: datetime) -> list[datetime]:
    days = (end - start).days
    return [start + timedelta(days=offset) for offset in range(days + 1)]


def build_trend_timeseries(data: list[dict[str, str]], term: str) -> list[dict[str, int | str]]:
    term_lower = term.lower()
    counts = defaultdict(int)
    dates = []

    for row in data:
        created_at = datetime.fromisoformat(row["created_at"])
        dates.append(created_at)
        content = row["content"].lower()
        if term_lower in content:
            counts[created_at.date()] += 1

    if not dates:
        return []

    start = min(dates).date()
    end = max(dates).date()

    series = []
    for day in _date_range(datetime.combine(start, datetime.min.time()), datetime.combine(end, datetime.min.time())):
        series.append({"date": day.strftime("%Y-%m-%d"), "count": counts[day.date()]})
    return series


def main() -> None:
    from data.preprocess_data import preprocess_data

    data = preprocess_data()
    trends = detect_trends(data)
    for trend in trends:
        series = build_trend_timeseries(data, trend)
        print(f"Trend: {trend}, sample points: {series[:3]}")


if __name__ == "__main__":
    main()
    print("Trend detection complete")
