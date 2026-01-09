# Development Guide

This document outlines the local workflows used to develop and validate the
project. All commands assume you are running from the repository root.

## Environment setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The project relies on the Python standard library, so installing
`requirements.txt` is effectively a no-op. It is included for parity with
common workflows.

## Generate sample data

```bash
python scripts/generate_sample_data.py
```

The script is deterministic. Re-running it always yields the same dataset.

## Preprocess data

```bash
python data/preprocess_data.py
```

This step validates the CSV schema, normalizes text, and produces
`data/processed_data.csv`.

## Train the baseline sentiment calibration

```bash
python -m models.save_model
```

The calibration JSON is stored in `models/sentiment_calibration.json`.

## Run the API server

```bash
./scripts/run.sh
```

Open `http://localhost:5000` in a browser to view the dashboard.

## Run tests

```bash
python -m unittest discover -s tests
```

## Run the full verification suite

```bash
./scripts/verify.sh
```

This command regenerates data, runs unit tests, starts the API server, and
executes a smoke test.

## Troubleshooting

### The dashboard shows empty charts

1. Confirm the API server is running with `curl http://localhost:5000/health`.
2. Confirm `data/processed_data.csv` exists. If not, run
   `python data/preprocess_data.py`.
3. Refresh the browser. The dashboard fetches data on load and does not cache
   results.

### `ModuleNotFoundError`

If you see import errors, ensure you are running the repository with a Python
3.11+ interpreter:

```bash
python --version
```

### Regenerating sample data

If you want a fresh dataset, delete `data/sample_data.csv` and rerun the
generator script:

```bash
rm data/sample_data.csv
python scripts/generate_sample_data.py
```

### Docker usage

To run the API in Docker:

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

The API will be available at `http://localhost:5000`.
