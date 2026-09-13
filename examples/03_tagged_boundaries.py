"""Etiquetar las cuatro fronteras de un rectángulo y comprobar sus medidas."""

from __future__ import annotations

import dolfinx
import numpy as np
import ufl
from dolfinx import mesh
from mpi4py import MPI

from mcandes_fenicsx.boundaries import tag_boundaries
from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import global_cell_count, global_scalar


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    length, height = 2.0, 1.0
    domain = mesh.create_rectangle(
        comm,
        [np.array([0.0, 0.0]), np.array([length, height])],
        (8 if args.quick else 20, 4 if args.quick else 10),
        cell_type=mesh.CellType.triangle,
    )
    tags = tag_boundaries(
        domain,
        {
            1: lambda x: np.isclose(x[0], 0.0),
            2: lambda x: np.isclose(x[0], length),
            3: lambda x: np.isclose(x[1], 0.0),
            4: lambda x: np.isclose(x[1], height),
        },
    )
    ds = ufl.Measure("ds", domain=domain, subdomain_data=tags)
    measured = {marker: global_scalar(1.0 * ds(marker), comm) for marker in range(1, 5)}
    expected = {1: height, 2: height, 3: length, 4: length}
    deviations = {marker: abs(measured[marker] - expected[marker]) for marker in expected}
    passed = max(deviations.values()) < 1.0e-12
    summary = {
        "example": "tagged-boundaries",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(domain),
        "boundary_measures": measured,
        "maximum_measure_error": max(deviations.values()),
        "solver_converged": True,
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError(f"medidas de frontera incorrectas: {measured}")


if __name__ == "__main__":
    main()
