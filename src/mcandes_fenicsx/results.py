"""Salida estructurada común a los ejemplos seriales y paralelos."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


def _json_value(value: Any) -> Any:
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("el resultado JSON no admite NaN ni infinito")
        return number
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


def emit_result(
    summary: dict[str, Any],
    output_dir: str | Path,
    *,
    rank: int = 0,
    print_json: bool = True,
) -> Path | None:
    """Validar, imprimir y guardar un resumen únicamente desde el rango raíz."""

    if rank != 0:
        return None
    required = {"example", "dolfinx_version", "mpi_size", "solver_converged", "validation_passed"}
    missing = sorted(required - summary.keys())
    if missing:
        raise ValueError(f"faltan claves de resultado: {', '.join(missing)}")
    safe = _json_value(summary)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / f"{safe['example']}.json"
    payload = json.dumps(safe, ensure_ascii=False, indent=2, sort_keys=True)
    path.write_text(f"{payload}\n", encoding="utf-8")
    if print_json:
        print(payload)
    return path
