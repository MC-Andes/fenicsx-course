#!/usr/bin/env python3
"""Verificar en CI que las rutas de ejemplos mencionadas en Markdown existen."""

from pathlib import Path

from mcandes_fenicsx.validation_cli import validate_repository

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    failures = validate_repository(root)
    for failure in failures:
        print(f"ERROR: {failure}")
    raise SystemExit(bool(failures))
