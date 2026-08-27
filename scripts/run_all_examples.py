#!/usr/bin/env python3
"""Ejecutar secuencialmente todos los ejemplos en modo de CI."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results/all"))
    parser.add_argument("--from-example", type=int, default=0)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    scripts = sorted((root / "examples").glob("[0-9][0-9]_*.py"))
    for script in scripts:
        number = int(script.name[:2])
        if number < args.from_example:
            continue
        print(f"RUN {script.relative_to(root)}", flush=True)
        subprocess.run(
            [sys.executable, str(script), "--quick", "--output", str(args.output)],
            cwd=root,
            check=True,
            timeout=300,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
