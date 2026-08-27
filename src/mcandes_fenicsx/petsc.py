"""Selecciones conservadoras de PETSc usadas en más de un ejemplo."""

from __future__ import annotations

from typing import Any


def direct_solver_options() -> dict[str, Any]:
    """Opciones portables: LU y error explícito, sin exigir un backend externo."""

    return {
        "ksp_type": "preonly",
        "pc_type": "lu",
        "ksp_error_if_not_converged": True,
    }


def nonlinear_solver_options() -> dict[str, Any]:
    """Newton con line search y fallos visibles."""

    return {
        "snes_type": "newtonls",
        "snes_linesearch_type": "bt",
        "snes_atol": 1.0e-9,
        "snes_rtol": 1.0e-8,
        "snes_max_it": 40,
        "snes_error_if_not_converged": True,
        "ksp_type": "preonly",
        "pc_type": "lu",
        "ksp_error_if_not_converged": True,
    }
