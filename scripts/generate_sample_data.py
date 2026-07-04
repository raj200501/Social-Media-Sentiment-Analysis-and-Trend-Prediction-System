import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_PATH = ROOT_DIR / "data" / "sample_data.csv"


platforms = ["twitter", "reddit", "mastodon", "instagram", "threads"]
positive_phrases = [
    "love the new update",
    "fantastic release",
    "excited for the feature",
    "great experience",
    "amazing support",
    "pleasant surprise",
    "solid improvement",
    "happy with the results",
]
negative_phrases = [
    "bad experience",
    "frustrating bug",
    "terrible outage",
    "disappointed with the update",
    "awful UI change",
    "slow performance",
    "confusing instructions",
    "unhappy with support",
]
neutral_phrases = [
    "reading the announcement",
    "checking the dashboard",
    "monitoring the rollout",
    "sharing the documentation",
    "running the demo",
    "reviewing the metrics",
    "attending the webinar",
    "noting the release schedule",
]
trend_terms = [
    "#ai",
    "#opensource",
    "#ml",
    "#dataviz",
    "#productivity",
    "#sustainability",
    "#security",
    "#cloud",
]

def generate_rows() -> list[dict[str, int | str]]:
    random.seed(42)
    start_date = datetime(2023, 1, 1)
    rows = []
    row_id = 1
    for day in range(0, 365):
        date = start_date + timedelta(days=day)
        for _ in range(4):
            sentiment_bucket = random.choices(
                ["positive", "negative", "neutral"], weights=[0.4, 0.2, 0.4]
            )[0]
            if sentiment_bucket == "positive":
                phrase = random.choice(positive_phrases)
            elif sentiment_bucket == "negative":
                phrase = random.choice(negative_phrases)
            else:
                phrase = random.choice(neutral_phrases)
            trend = random.choice(trend_terms)
            platform = random.choice(platforms)
            content = f"{phrase} {trend} on {platform}."
            likes = random.randint(0, 500)
            shares = random.randint(0, 200)
            rows.append(
                {
                    "id": row_id,
                    "created_at": date.strftime("%Y-%m-%d"),
                    "platform": platform,
                    "content": content,
                    "likes": likes,
                    "shares": shares,
                }
            )
            row_id += 1
    return rows


def write_rows(rows: list[dict[str, int | str]], output_path: Path = DEFAULT_OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "created_at", "platform", "content", "likes", "shares"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = generate_rows()
    write_rows(rows)
    print(f"Wrote {len(rows)} rows to {DEFAULT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
