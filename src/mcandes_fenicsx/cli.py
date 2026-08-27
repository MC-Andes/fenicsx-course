"""Argumentos compartidos sin ocultar la formulación de cada demostración."""

from __future__ import annotations

import argparse
from pathlib import Path


def example_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--quick", action="store_true", help="malla/tiempo reducido para CI")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results"),
        help="directorio para JSON y campos de salida",
    )
    parser.add_argument("--write-fields", action="store_true", help="escribir XDMF para ParaView")
    return parser
