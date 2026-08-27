"""Comprobar versiones, MPI y construcción básica de una malla DOLFINx."""

from __future__ import annotations

import basix
import dolfinx
import ffcx
import mpi4py
import petsc4py
import ufl
from dolfinx import mesh
from mpi4py import MPI

from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import global_cell_count


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    domain = mesh.create_unit_square(comm, 2, 2)
    cells = global_cell_count(domain)
    passed = cells == 8
    summary = {
        "example": "sanity-check",
        "dolfinx_version": dolfinx.__version__,
        "basix_version": basix.__version__,
        "ffcx_version": ffcx.__version__,
        "ufl_version": ufl.__version__,
        "mpi4py_version": mpi4py.__version__,
        "petsc4py_version": petsc4py.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": cells,
        "solver_converged": True,
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError(f"se esperaban 8 celdas globales y se obtuvieron {cells}")


if __name__ == "__main__":
    main()
