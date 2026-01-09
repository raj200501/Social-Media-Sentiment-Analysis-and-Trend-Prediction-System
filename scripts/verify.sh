#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python scripts/generate_sample_data.py
python data/preprocess_data.py
python -m models.save_model

python -m unittest discover -s tests

python -m api.api_server &
SERVER_PID=$!
trap 'kill ${SERVER_PID} >/dev/null 2>&1 || true' EXIT

python scripts/wait_for_server.py http://localhost:5000/health
python scripts/smoke_test.py
