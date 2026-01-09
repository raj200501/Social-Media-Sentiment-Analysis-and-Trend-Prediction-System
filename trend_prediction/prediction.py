"""Forecast trend volume using a simple linear regression."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from data.preprocess_data import preprocess_data
from trend_detection.trend_detection import build_trend_timeseries


@dataclass(frozen=True)
class TrendForecast:
    term: str
    history: list[dict[str, int | str]]
    forecast: list[dict[str, float | str]]


def fit_linear_regression(values: Iterable[int | float]) -> tuple[float, float]:
    y = [float(value) for value in values]
    n = len(y)
    if n == 0:
        raise ValueError("Cannot fit regression with no data")
    if n == 1:
        return y[0], 0.0

    x = list(range(n))
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xx = sum(value * value for value in x)
    sum_xy = sum(x[i] * y[i] for i in range(n))

    denominator = n * sum_xx - sum_x * sum_x
    if denominator == 0:
        slope = 0.0
    else:
        slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    return intercept, slope


def predict_trend_counts(history: list[dict[str, int | str]], horizon: int = 7) -> list[dict[str, float | str]]:
    counts = [point["count"] for point in history]
    intercept, slope = fit_linear_regression(counts)

    forecast = []
    for step in range(1, horizon + 1):
        prediction = max(0.0, intercept + slope * (len(counts) + step - 1))
        forecast.append({"day": step, "count": round(prediction, 2)})

    return forecast


def predict_trend(
    term: str,
    data_path: str | Path = Path("data/sample_data.csv"),
    output_path: str | Path | None = Path("data/processed_data.csv"),
    horizon: int = 7,
) -> TrendForecast:
    input_path = Path(data_path)
    if output_path is None:
        output_path = input_path.with_name("processed_data.csv")

    data = preprocess_data(input_path=input_path, output_path=Path(output_path))
    history = build_trend_timeseries(data, term)
    forecast = predict_trend_counts(history, horizon=horizon)
    return TrendForecast(term=term, history=history, forecast=forecast)


def main() -> None:
    forecast = predict_trend("#ai")
    print(f"Trend forecast for {forecast.term}:")
    print(forecast.forecast[:5])


if __name__ == "__main__":
    main()
    print("Trend prediction complete")
