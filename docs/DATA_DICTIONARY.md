# Data Dictionary

This document describes the schema for the CSV datasets used in this project.
All column names are lowercase with underscores, and values are generated in a
deterministic way by `scripts/generate_sample_data.py`.

## Raw dataset (`data/sample_data.csv`)

| Column | Type | Description | Example |
| --- | --- | --- | --- |
| `id` | integer | Stable identifier for each post. Sequential in the synthetic dataset. | `42` |
| `created_at` | date | Date of the post in ISO format. | `2023-05-18` |
| `platform` | string | The platform where the post originated. | `twitter` |
| `content` | string | Short text content including a hashtag. | `"love the new update #ai"` |
| `likes` | integer | Simulated like count. | `133` |
| `shares` | integer | Simulated share/retweet count. | `57` |

### Sample row

```csv
id,created_at,platform,content,likes,shares
1,2023-01-01,twitter,Love the new update #ai on twitter.,121,45
```

## Processed dataset (`data/processed_data.csv`)

The processed dataset retains all raw columns and adds two fields:

| Column | Type | Description | Example |
| --- | --- | --- | --- |
| `cleaned_content` | string | Normalized lowercase content. | `"love the new update #ai on twitter"` |
| `tokens` | array-like string | Tokenized representation of content stored as JSON. | `"[\"love\", \"the\", \"new\", \"update\", \"#ai\"]"` |

### Column notes

- `cleaned_content` is produced by `data.preprocess_data.normalize_text`.
- `tokens` is the output of the tokenizer, stored as a JSON string when written
  to CSV.

## Derived fields in the API

Several endpoints generate fields on the fly:

- `sentiment` (float): sentiment score computed for each post using
  `sentiment_analysis.sentiment.analyze_sentiment`.
- `score` (float): the daily average sentiment reported by
  `/api/sentiment_data`.
- `series` (array): daily counts for the selected trend term.
- `forecast` (array): predicted counts for future days from the linear
  regression model.

## Data lifecycle

1. `scripts/generate_sample_data.py` writes the raw dataset.
2. `data/preprocess_data.py` validates and enriches the dataset.
3. The API loads the processed dataset and serves derived metrics.

## Determinism

Because the generator uses a fixed random seed, the dataset is identical for
all users. This makes unit tests and smoke tests repeatable, and ensures the
trend detection output does not change between runs.
