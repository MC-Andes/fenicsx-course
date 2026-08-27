"""Cálculos de verificación reproducibles y seguros bajo MPI."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any


def convergence_rates(mesh_sizes: Sequence[float], errors: Sequence[float]) -> list[float]:
    """Calcular tasas entre pares consecutivos, sin suponer refinamiento uniforme."""

    if len(mesh_sizes) != len(errors) or len(errors) < 2:
        raise ValueError("se requieren listas del mismo tamaño con al menos dos valores")
    if any(value <= 0 for value in (*mesh_sizes, *errors)):
        raise ValueError("tamaños de malla y errores deben ser positivos")
    rates: list[float] = []
    for index in range(1, len(errors)):
        numerator = math.log(errors[index] / errors[index - 1])
        denominator = math.log(mesh_sizes[index] / mesh_sizes[index - 1])
        if math.isclose(denominator, 0.0):
            raise ValueError("dos tamaños de malla consecutivos son iguales")
        rates.append(numerator / denominator)
    return rates


def global_scalar(form_expression: Any, comm: Any) -> float:
    """Ensamblar una integral y sumar las contribuciones de todos los rangos."""

    from dolfinx import fem
    from mpi4py import MPI

    local = fem.assemble_scalar(fem.form(form_expression))
    return float(comm.allreduce(local, op=MPI.SUM).real)


def global_l2_error(approximation: Any, exact: Any) -> float:
    """Norma L2 global de un error escalar o vectorial."""

    import ufl

    difference = approximation - exact
    inner: Any = ufl.inner
    squared = global_scalar(
        inner(difference, difference) * ufl.dx,
        approximation.function_space.mesh.comm,
    )
    return math.sqrt(max(squared, 0.0))


def global_h1_seminorm_error(approximation: Any, exact: Any) -> float:
    """Seminorma H1 global del error."""

    import ufl

    difference = approximation - exact
    inner: Any = ufl.inner
    gradient: Any = ufl.grad
    squared = global_scalar(
        inner(gradient(difference), gradient(difference)) * ufl.dx,
        approximation.function_space.mesh.comm,
    )
    return math.sqrt(max(squared, 0.0))


def global_cell_count(mesh: Any) -> int:
    """Número global de celdas propias, sin contar fantasmas."""

    from mpi4py import MPI

    cell_map = mesh.topology.index_map(mesh.topology.dim)
    return int(mesh.comm.allreduce(cell_map.size_local, op=MPI.SUM))


def require_solver_convergence(solver: Any, label: str = "PETSc") -> int:
    """Fallar de forma explícita si KSP o SNES no convergió."""

    reason = int(solver.getConvergedReason())
    if reason <= 0:
        raise RuntimeError(f"{label} no convergió; razón PETSc={reason}")
    return reason


def relative_difference(value: float, reference: float, floor: float = 1.0e-15) -> float:
    """Diferencia relativa estable cerca de cero."""

    return abs(value - reference) / max(abs(reference), floor)
