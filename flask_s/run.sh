#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ -f ../.env ]; then
  set -a
  # shellcheck disable=SC1091
  . ../.env
  set +a
elif [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . .env
  set +a
fi
uv sync
uv run python app.py
