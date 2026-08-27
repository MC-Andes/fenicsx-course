"""Interpolar un campo analítico en P1/P2 y medir convergencia L2 global."""

from __future__ import annotations

import dolfinx
import numpy as np
import ufl
from dolfinx import fem, mesh
from mpi4py import MPI

from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import convergence_rates, global_l2_error


def interpolate_error(n: int, degree: int) -> float:
    domain = mesh.create_unit_square(MPI.COMM_WORLD, n, n)
    space = fem.functionspace(domain, ("Lagrange", degree))
    field = fem.Function(space, name=f"interpolante_P{degree}")
    field.interpolate(lambda x: np.sin(np.pi * x[0]) * np.sin(np.pi * x[1]))
    field.x.scatter_forward()

    # Estos objetos son simbólicos; no son arreglos de valores evaluados.
    trial = ufl.TrialFunction(space)
    test = ufl.TestFunction(space)
    _mass_form = ufl.inner(trial, test) * ufl.dx
    x = ufl.SpatialCoordinate(domain)
    exact = ufl.sin(ufl.pi * x[0]) * ufl.sin(ufl.pi * x[1])
    return global_l2_error(field, exact)


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    refinements = [8, 16] if args.quick else [8, 16, 32]
    errors: dict[str, list[float]] = {}
    rates: dict[str, list[float]] = {}
    for degree in (1, 2):
        key = f"P{degree}"
        errors[key] = [interpolate_error(n, degree) for n in refinements]
        rates[key] = convergence_rates([1.0 / n for n in refinements], errors[key])

    passed = rates["P1"][-1] > 1.7 and rates["P2"][-1] > 2.5
    summary = {
        "example": "interpolation",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "refinements": refinements,
        "l2_errors": errors,
        "rates": rates,
        "solver_converged": True,
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError(f"tasas de interpolación inesperadas: {rates}")


if __name__ == "__main__":
    main()
