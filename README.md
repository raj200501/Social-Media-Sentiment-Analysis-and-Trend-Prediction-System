# Social Media Sentiment Analysis and Trend Prediction System

This repository contains a runnable system that ingests social media-style
posts, analyzes sentiment, detects trending topics, forecasts trend volume, and
serves a lightweight dashboard. The implementation is intentionally
lightweight and deterministic so it can run in a clean Python environment
without heavyweight ML dependencies.

## Features

- Rule-based sentiment analysis with transparent scoring
- Trend detection based on term frequency
- Linear regression trend forecasting
- JSON API + static dashboard (served by the API)
- Deterministic synthetic dataset and reproducible verification
- Xquik CSV, JSON, or JSONL export import for real tweet analysis

## Prerequisites

- Python 3.11+
- (Optional) Docker + Docker Compose

## Verified Quickstart

The following commands were executed successfully to launch the system:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/generate_sample_data.py
python data/preprocess_data.py
./scripts/run.sh
```

Then open the dashboard at `http://localhost:5000`.

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/health` | GET | Health check used by tests and CI. |
| `/api/sentiment` | POST | Analyze sentiment for a single post. |
| `/api/sentiment_data` | GET | Daily average sentiment series. |
| `/api/trend_data` | GET | Top trend and its daily counts. |
| `/api/predict` | POST | Forecast trend counts for a given term. |

Example request:

```bash
curl -X POST http://localhost:5000/api/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"I love the new update"}'
```

## Verified Verification

Run the full deterministic verification suite:

```bash
./scripts/verify.sh
```

The script:

1. Regenerates the synthetic dataset.
2. Runs unit tests.
3. Starts the API server.
4. Executes an API smoke test.

## Xquik Export Import

Use the importer when you want to replace the synthetic sample data with tweet
rows exported from Xquik:

```bash
python scripts/import_xquik_export.py path/to/xquik-export.jsonl
python data/preprocess_data.py
./scripts/run.sh
```

The importer accepts CSV, JSON, and JSONL files. It maps common Xquik export
fields such as `text`, `content`, `full_text`, `created_at`, `like_count`, and
`retweet_count` into this project's `data/sample_data.csv` schema. Rows without
tweet text are skipped, duplicate tweet identifiers are ignored, and missing
engagement counts default to `0`.

## Docker (Optional)

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

The API will be available at `http://localhost:5000`.

## Project documentation

- [Architecture overview](docs/ARCHITECTURE.md)
- [Data dictionary](docs/DATA_DICTIONARY.md)
- [Development guide](docs/DEVELOPMENT.md)

## License

This project is licensed under the MIT License.
