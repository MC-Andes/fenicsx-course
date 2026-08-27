#!/usr/bin/env bash
set -euo pipefail

ruff check .
pytest tests/unit
python scripts/validate_examples.py
mkdocs build --strict
