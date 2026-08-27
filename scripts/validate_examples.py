#!/usr/bin/env python3
"""Compatibilidad: ejecutar el validador desde un checkout sin instalar scripts."""

from mcandes_fenicsx.validation_cli import main

if __name__ == "__main__":
    raise SystemExit(main())
