"""HTTP API server for sentiment analysis and trend prediction."""
from __future__ import annotations

from dataclasses import asdict
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
from typing import Any

from data.preprocess_data import preprocess_data
from sentiment_analysis.sentiment import analyze_sentiment
from trend_detection.trend_detection import build_trend_timeseries, detect_trends
from trend_prediction.prediction import predict_trend

DEFAULT_DATA_PATH = Path("data/processed_data.csv")
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@lru_cache(maxsize=1)
def load_dataset() -> list[dict[str, str]]:
    return preprocess_data(output_path=DEFAULT_DATA_PATH)


def json_response(handler: BaseHTTPRequestHandler, payload: Any, status: int = 200) -> None:
    data = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def error_response(handler: BaseHTTPRequestHandler, message: str, status: int = 400) -> None:
    json_response(handler, {"error": message}, status=status)


def parse_json(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    payload = handler.rfile.read(length)
    try:
        return json.loads(payload.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def sentiment_series(data: list[dict[str, str]]) -> list[dict[str, float | str]]:
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}

    for row in data:
        date = row["created_at"]
        score = analyze_sentiment(row["content"]).score
        totals[date] = totals.get(date, 0.0) + score
        counts[date] = counts.get(date, 0) + 1

    series = [
        {"date": date, "score": round(totals[date] / counts[date], 3)}
        for date in sorted(totals)
    ]
    return series


class SentimentHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path == "/health":
            return json_response(self, {"status": "ok"})

        if self.path == "/api/sentiment_data":
            data = load_dataset()
            return json_response(self, sentiment_series(data))

        if self.path == "/api/trend_data":
            data = load_dataset()
            trends = detect_trends(data)
            if not trends:
                return error_response(self, "No trends detected", status=404)
            top_trend = trends[0]
            series = build_trend_timeseries(data, top_trend)
            return json_response(self, {"trend": top_trend, "series": series})

        if self.path == "/" or self.path == "/index.html":
            return self._serve_static("index.html")

        if self.path.startswith("/api/"):
            return error_response(self, "Not found", status=404)

        if self.path.startswith("/"):
            filename = self.path.lstrip("/")
            return self._serve_static(filename)

        return error_response(self, "Not found", status=404)

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path == "/api/sentiment":
            payload = parse_json(self)
            text = payload.get("text")
            if not text:
                return error_response(self, "Missing required field: text")
            result = analyze_sentiment(text)
            return json_response(self, {"result": asdict(result)})

        if self.path == "/api/predict":
            payload = parse_json(self)
            term = payload.get("trend")
            days = payload.get("days", 7)
            try:
                days = int(days)
            except (TypeError, ValueError):
                return error_response(self, "days must be an integer")

            if days < 1 or days > 30:
                return error_response(self, "days must be between 1 and 30")

            if term is None:
                data = load_dataset()
                trends = detect_trends(data)
                if not trends:
                    return error_response(self, "No trends available for prediction", status=404)
                term = trends[0]

            forecast = predict_trend(term, horizon=days)
            return json_response(
                self,
                {
                    "term": forecast.term,
                    "history": forecast.history,
                    "forecast": forecast.forecast,
                },
            )

        return error_response(self, "Not found", status=404)

    def _serve_static(self, filename: str) -> None:
        file_path = FRONTEND_DIR / filename
        if not file_path.exists() or not file_path.is_file():
            return error_response(self, "Not found", status=404)
        content_type, _ = mimetypes.guess_type(str(file_path))
        content_type = content_type or "application/octet-stream"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003 - match base class
        return


def run_server(host: str = "0.0.0.0", port: int = 5000) -> None:
    server = ThreadingHTTPServer((host, port), SentimentHandler)
    print(f"Server running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
