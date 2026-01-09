#!/usr/bin/env bash
set -euo pipefail

python data/preprocess_data.py
python -m api.api_server
