"""Resolver Poisson manufacturado y verificar tasas L2/H1 para P1."""

from __future__ import annotations

import dolfinx
import numpy as np
import ufl
from dolfinx import fem, io, mesh
from dolfinx.fem.petsc import LinearProblem
from mpi4py import MPI
from petsc4py import PETSc

from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.petsc import direct_solver_options
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import (
    convergence_rates,
    global_cell_count,
    global_h1_seminorm_error,
    global_l2_error,
    require_solver_convergence,
)


def solve_poisson(n: int) -> tuple[fem.Function, float, float, int]:
    domain = mesh.create_unit_square(MPI.COMM_WORLD, n, n, mesh.CellType.triangle)
    space = fem.functionspace(domain, ("Lagrange", 1))
    u, v = ufl.TrialFunction(space), ufl.TestFunction(space)
    x = ufl.SpatialCoordinate(domain)
    exact = ufl.sin(ufl.pi * x[0]) * ufl.sin(ufl.pi * x[1])
    source = 2.0 * ufl.pi**2 * exact
    boundary_facets = mesh.locate_entities_boundary(
        domain, domain.topology.dim - 1, lambda points: np.full(points.shape[1], True)
    )
    dofs = fem.locate_dofs_topological(space, domain.topology.dim - 1, boundary_facets)
    bc = fem.dirichletbc(PETSc.ScalarType(0.0), dofs, space)
    problem = LinearProblem(
        ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx,
        ufl.inner(source, v) * ufl.dx,
        bcs=[bc],
        petsc_options_prefix=f"mcandes_poisson_{n}_",
        petsc_options=direct_solver_options(),
    )
    solution = problem.solve()
    solution.name = "u_h"
    solution.x.scatter_forward()
    reason = require_solver_convergence(problem.solver, "Poisson KSP")
    return (
        solution,
        global_l2_error(solution, exact),
        global_h1_seminorm_error(solution, exact),
        reason,
    )


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    refinements = [8, 16] if args.quick else [8, 16, 32]
    l2_errors: list[float] = []
    h1_errors: list[float] = []
    reasons: list[int] = []
    last_solution: fem.Function | None = None
    for n in refinements:
        last_solution, l2_error, h1_error, reason = solve_poisson(n)
        l2_errors.append(l2_error)
        h1_errors.append(h1_error)
        reasons.append(reason)
    mesh_sizes = [1.0 / n for n in refinements]
    l2_rates = convergence_rates(mesh_sizes, l2_errors)
    h1_rates = convergence_rates(mesh_sizes, h1_errors)
    passed = l2_rates[-1] > 1.8 and h1_rates[-1] > 0.9 and all(reason > 0 for reason in reasons)

    if args.write_fields and last_solution is not None:
        field_dir = args.output / "poisson"
        if comm.rank == 0:
            field_dir.mkdir(parents=True, exist_ok=True)
        comm.barrier()
        with io.XDMFFile(comm, field_dir / "solution.xdmf", "w") as xdmf:
            xdmf.write_mesh(last_solution.function_space.mesh)
            xdmf.write_function(last_solution)

    summary = {
        "example": "poisson-manufactured",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(last_solution.function_space.mesh),
        "refinements": refinements,
        "l2_errors": l2_errors,
        "h1_seminorm_errors": h1_errors,
        "l2_rates": l2_rates,
        "h1_rates": h1_rates,
        "solver_reasons": reasons,
        "solver_converged": all(reason > 0 for reason in reasons),
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError(f"convergencia fuera de lo esperado: L2={l2_rates}, H1={h1_rates}")


if __name__ == "__main__":
    main()
