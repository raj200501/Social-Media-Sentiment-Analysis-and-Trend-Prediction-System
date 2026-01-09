"""Rule-based sentiment analysis utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from data.preprocess_data import tokenize
from sentiment_analysis.lexicon import NEGATIVE_WORDS, POSITIVE_WORDS


@dataclass(frozen=True)
class SentimentResult:
    score: float
    label: str
    positive_hits: int
    negative_hits: int


LABEL_THRESHOLDS = {
    "positive": 0.2,
    "negative": -0.2,
}


def score_tokens(tokens: Iterable[str]) -> SentimentResult:
    tokens = list(tokens)
    if not tokens:
        return SentimentResult(score=0.0, label="neutral", positive_hits=0, negative_hits=0)

    positive_hits = sum(1 for token in tokens if token in POSITIVE_WORDS)
    negative_hits = sum(1 for token in tokens if token in NEGATIVE_WORDS)
    raw_score = (positive_hits - negative_hits) / max(len(tokens), 1)

    if raw_score >= LABEL_THRESHOLDS["positive"]:
        label = "positive"
    elif raw_score <= LABEL_THRESHOLDS["negative"]:
        label = "negative"
    else:
        label = "neutral"

    return SentimentResult(
        score=round(raw_score, 3),
        label=label,
        positive_hits=positive_hits,
        negative_hits=negative_hits,
    )


def analyze_sentiment(text: str) -> SentimentResult:
    tokens = tokenize(text)
    return score_tokens(tokens)


def analyze_sentiment_batch(texts: Iterable[str]) -> list[SentimentResult]:
    return [analyze_sentiment(text) for text in texts]
