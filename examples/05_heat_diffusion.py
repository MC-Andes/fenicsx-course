"""Difusión con Euler implícito, solución analítica y disipación de energía."""

from __future__ import annotations

import math

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
    global_cell_count,
    global_l2_error,
    global_scalar,
    require_solver_convergence,
)


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    n = 16 if args.quick else 32
    steps = 10 if args.quick else 50
    final_time = 0.05
    dt_value = final_time / steps
    domain = mesh.create_unit_square(comm, n, n)
    space = fem.functionspace(domain, ("Lagrange", 1))
    previous = fem.Function(space, name="temperature_previous")
    previous.interpolate(lambda x: np.sin(np.pi * x[0]) * np.sin(np.pi * x[1]))
    previous.x.scatter_forward()
    initial_energy = 0.5 * global_scalar(ufl.inner(previous, previous) * ufl.dx, comm)

    trial, test = ufl.TrialFunction(space), ufl.TestFunction(space)
    dt = fem.Constant(domain, PETSc.ScalarType(dt_value))
    bilinear = ufl.inner(trial, test) * ufl.dx + dt * ufl.inner(ufl.grad(trial), ufl.grad(test)) * ufl.dx
    linear = ufl.inner(previous, test) * ufl.dx
    facets = mesh.locate_entities_boundary(
        domain, domain.topology.dim - 1, lambda x: np.full(x.shape[1], True)
    )
    dofs = fem.locate_dofs_topological(space, domain.topology.dim - 1, facets)
    bc = fem.dirichletbc(PETSc.ScalarType(0.0), dofs, space)
    problem = LinearProblem(
        bilinear,
        linear,
        bcs=[bc],
        petsc_options_prefix="mcandes_heat_",
        petsc_options=direct_solver_options(),
    )
    reasons: list[int] = []
    solution: fem.Function | None = None
    for _ in range(steps):
        solution = problem.solve()
        solution.x.scatter_forward()
        reasons.append(require_solver_convergence(problem.solver, "difusión KSP"))
        previous.x.array[:] = solution.x.array
        previous.x.scatter_forward()

    assert solution is not None
    solution.name = "temperature"
    x = ufl.SpatialCoordinate(domain)
    exact = math.exp(-2.0 * math.pi**2 * final_time) * ufl.sin(ufl.pi * x[0]) * ufl.sin(ufl.pi * x[1])
    l2_error = global_l2_error(solution, exact)
    final_energy = 0.5 * global_scalar(ufl.inner(solution, solution) * ufl.dx, comm)
    passed = l2_error < 3.0e-2 and final_energy < initial_energy and all(reason > 0 for reason in reasons)

    if args.write_fields:
        field_dir = args.output / "heat"
        if comm.rank == 0:
            field_dir.mkdir(parents=True, exist_ok=True)
        comm.barrier()
        with io.XDMFFile(comm, field_dir / "temperature.xdmf", "w") as xdmf:
            xdmf.write_mesh(domain)
            xdmf.write_function(solution, final_time)

    summary = {
        "example": "heat-diffusion",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(domain),
        "time_steps": steps,
        "final_time": final_time,
        "l2_error": l2_error,
        "initial_energy": initial_energy,
        "final_energy": final_energy,
        "solver_converged": all(reason > 0 for reason in reasons),
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError("la difusión no satisface error/disipación esperados")


if __name__ == "__main__":
    main()
