# Architecture Overview

This project is intentionally lightweight so it can run in a clean Python
environment without heavyweight machine learning dependencies. The system still
models the core pipeline described in the README: data ingestion, sentiment
analysis, trend detection, trend forecasting, and a dashboard for the results.

## High-level flow

1. **Raw data ingestion**
   - Input lives in `data/sample_data.csv`.
   - `scripts/generate_sample_data.py` can regenerate the synthetic dataset in a
     deterministic way.
2. **Preprocessing**
   - `data/preprocess_data.py` normalizes text, tokenizes content, validates
     required columns, and writes the processed dataset to
     `data/processed_data.csv`.
3. **Sentiment analysis**
   - `sentiment_analysis/lexicon.py` contains curated positive and negative
     word lists.
   - `sentiment_analysis/sentiment.py` computes sentiment scores and labels
     using a rule-based scoring approach.
4. **Trend detection**
   - `trend_detection/trend_detection.py` extracts terms from content, removes
     stop words, and returns ranked trends along with time series data.
5. **Trend prediction**
   - `trend_prediction/prediction.py` uses a simple linear regression to
     forecast future counts based on the historical trend series.
6. **API + dashboard**
   - `api/api_server.py` serves JSON endpoints and a static dashboard
     (`frontend/`), allowing the system to be used locally without any
     additional dependencies.

## Directory map

```
api/
  api_server.py         HTTP entrypoint + static file serving

data/
  sample_data.csv       Synthetic dataset (source of truth)
  processed_data.csv    Generated during preprocessing
  load_data.py          CSV loader utility
  preprocess_data.py    Cleaning + tokenization

frontend/
  index.html            Static dashboard
  app.js                Fetches API data and renders charts
  style.css             Basic styling

sentiment_analysis/
  lexicon.py            Positive/negative word lists
  sentiment.py          Sentiment scoring functions
  model_training.py     Baseline calibration workflow

trend_detection/
  trend_detection.py    Term extraction and time-series aggregation
  trend_analysis.py     Generates a readable trend report

trend_prediction/
  prediction.py         Linear regression forecasting

models/
  save_model.py         Writes calibration JSON
  load_model.py         Reads calibration JSON

scripts/
  run.sh                Start the API + dashboard
  verify.sh             Deterministic verification used by CI
  smoke_test.py         API smoke test
  wait_for_server.py    Helper for readiness checks
  generate_sample_data.py  Synthetic data generator

 docs/
  ARCHITECTURE.md       This document
  DATA_DICTIONARY.md    Dataset schema and sample values
  DEVELOPMENT.md        Developer workflows and debugging tips
```

## Data design

The synthetic dataset intentionally mimics social media streams:

- A full year of daily data with multiple posts per day.
- Short text snippets with hashtags to drive trend analysis.
- Engagement metrics (likes, shares) for potential future extension.

The data is designed to support deterministic tests. By using a fixed random
seed, `scripts/generate_sample_data.py` produces identical datasets whenever it
runs, which keeps trend detection and sentiment scoring stable across runs.

## Sentiment scoring

The scoring system is intentionally transparent:

- Each token is compared against curated lexicons.
- The sentiment score is computed as:

```
(score) = (positive_hits - negative_hits) / total_tokens
```

- Scores are mapped to labels with thresholds:
  - **positive**: score >= 0.2
  - **negative**: score <= -0.2
  - **neutral**: otherwise

Because this logic is deterministic, it is easy to test and reason about.

## Trend detection

Trend detection is based on frequency analysis rather than probabilistic topic
models. This keeps the pipeline lightweight while still offering interpretable
results.

Key steps:

1. Tokenize the raw content into terms.
2. Remove common stop words.
3. Rank terms by frequency.
4. Select the top N terms above a configurable minimum count.
5. Build a daily time series for each trend term.

This approach is suitable for the synthetic dataset and provides reproducible
output for dashboards and tests.

## Trend prediction

A simple linear regression forecast is sufficient for this project. It follows
these steps:

1. Build the historical time series for a trend term.
2. Fit a line to the series using the closed-form least squares formula.
3. Extrapolate a configurable number of days into the future.

The forecast output is easy to interpret and is deterministic for the given
input data.

## API and dashboard

The API server uses Python's built-in `http.server` module. It exposes:

- `/health` for readiness checks.
- `/api/sentiment` for single-post sentiment analysis.
- `/api/sentiment_data` for daily average sentiment scores.
- `/api/trend_data` for the top detected trend and its time series.
- `/api/predict` for forecasting the top trend.

The same server hosts the static dashboard from `frontend/`, so users can load
`http://localhost:5000` and get an interactive visualization without any
additional tooling.

## Extensibility

The system is intentionally modular. Each part of the pipeline can be replaced
with more advanced models later. For example:

- Swap out the lexicon-based scorer for a transformer model.
- Replace frequency-based trend detection with topic modeling.
- Use time-series forecasting libraries such as Prophet or ARIMA.
- Persist data to a database instead of CSV files.

The provided modules and tests ensure a stable baseline, while the structure
makes it straightforward to extend the functionality.
