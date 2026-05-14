#!/usr/bin/env bash
# Fetch Parquet files from S3 stage bucket for local Evidence dev.
# Run this instead of the full pipeline convert step when data is already
# uploaded to S3.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/.."

cd "$ROOT/pipeline"

if ! command -v uv &>/dev/null; then
  echo "Error: uv not found. Install from https://github.com/astral-sh/uv" >&2
  exit 1
fi

uv sync --quiet
uv run python -m short_sales_pipeline.cli fetch \
  --parquet-dir "$ROOT/data/parquet" \
  "$@"
