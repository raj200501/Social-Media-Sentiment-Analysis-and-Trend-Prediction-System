"""Run a smoke test against the running API server."""
from __future__ import annotations

import json
from urllib.request import Request, urlopen

BASE_URL = "http://localhost:5000"


def request_json(path: str, method: str = "GET", payload: dict | None = None) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(f"{BASE_URL}{path}", data=data, headers=headers, method=method)
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    health = request_json("/health")
    if health.get("status") != "ok":
        raise SystemExit("Health check failed")

    sentiment = request_json("/api/sentiment", method="POST", payload={"text": "I love this"})
    if "result" not in sentiment:
        raise SystemExit("Sentiment response missing expected fields")

    sentiment_data = request_json("/api/sentiment_data")
    if not sentiment_data:
        raise SystemExit("Sentiment series is empty")

    trend_data = request_json("/api/trend_data")
    trend = trend_data.get("trend")
    if not trend:
        raise SystemExit("Trend data missing trend")

    forecast = request_json("/api/predict", method="POST", payload={"trend": trend, "days": 5})
    if len(forecast.get("forecast", [])) != 5:
        raise SystemExit("Forecast length mismatch")

    print("Smoke test passed")


if __name__ == "__main__":
    main()
