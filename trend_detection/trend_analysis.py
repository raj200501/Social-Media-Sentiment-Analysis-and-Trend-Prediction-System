"""Generate a textual trend report."""
from __future__ import annotations

from data.preprocess_data import preprocess_data
from trend_detection.trend_detection import build_trend_timeseries, detect_trends


def generate_trend_report() -> str:
    data = preprocess_data()
    trends = detect_trends(data)
    if not trends:
        return "No trends detected."

    lines = []
    for trend in trends:
        series = build_trend_timeseries(data, trend)
        total_mentions = sum(point["count"] for point in series)
        lines.append(f"Trend {trend}: {total_mentions} mentions")
    return "\n".join(lines)


def main() -> None:
    print(generate_trend_report())


if __name__ == "__main__":
    main()
    print("Trend analysis complete")
