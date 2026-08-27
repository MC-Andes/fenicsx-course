"""Placa rectangular elástica: reacción, energía y balance de fuerza."""

from __future__ import annotations

import dolfinx
import numpy as np
import ufl
from dolfinx import fem, io, mesh
from dolfinx.fem.petsc import LinearProblem
from mpi4py import MPI
from petsc4py import PETSc

from mcandes_fenicsx.boundaries import tag_boundaries
from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.petsc import direct_solver_options
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import (
    global_cell_count,
    global_scalar,
    relative_difference,
    require_solver_convergence,
)


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    length, height = 1.0, 0.2
    domain = mesh.create_rectangle(
        comm,
        [np.array([0.0, 0.0]), np.array([length, height])],
        (20 if args.quick else 60, 4 if args.quick else 12),
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
    space = fem.functionspace(domain, ("Lagrange", 2, (2,)))
    trial, test = ufl.TrialFunction(space), ufl.TestFunction(space)
    young, poisson = 100.0, 0.3
    mu = young / (2.0 * (1.0 + poisson))
    lambda_3d = young * poisson / ((1.0 + poisson) * (1.0 - 2.0 * poisson))
    lambda_plane_stress = 2.0 * mu * lambda_3d / (lambda_3d + 2.0 * mu)

    def strain(displacement: ufl.core.expr.Expr) -> ufl.core.expr.Expr:
        return ufl.sym(ufl.grad(displacement))

    def stress(displacement: ufl.core.expr.Expr) -> ufl.core.expr.Expr:
        return 2.0 * mu * strain(displacement) + lambda_plane_stress * ufl.tr(strain(displacement)) * ufl.Identity(2)

    traction_value = 1.0
    traction = fem.Constant(domain, (PETSc.ScalarType(traction_value), PETSc.ScalarType(0.0)))
    left_facets = tags.find(1)
    left_dofs = fem.locate_dofs_topological(space, domain.topology.dim - 1, left_facets)
    bc = fem.dirichletbc(np.zeros(2, dtype=PETSc.ScalarType), left_dofs, space)
    problem = LinearProblem(
        ufl.inner(stress(trial), strain(test)) * ufl.dx,
        ufl.inner(traction, test) * ds(2),
        bcs=[bc],
        petsc_options_prefix="mcandes_elasticity_",
        petsc_options=direct_solver_options(),
    )
    displacement = problem.solve()
    displacement.name = "displacement"
    displacement.x.scatter_forward()
    reason = require_solver_convergence(problem.solver, "elasticidad KSP")
    normal = ufl.FacetNormal(domain)
    boundary_reaction_x = global_scalar(
        ufl.dot(stress(displacement), normal)[0] * ds(1), comm
    )
    virtual_left_translation = fem.Function(space)
    virtual_left_translation.interpolate(
        lambda x: np.vstack((np.isclose(x[0], 0.0).astype(float), np.zeros(x.shape[1])))
    )
    reaction_x = global_scalar(
        ufl.inner(stress(displacement), strain(virtual_left_translation)) * ufl.dx
        - ufl.inner(traction, virtual_left_translation) * ds(2),
        comm,
    )
    external_x = traction_value * height
    balance_error = relative_difference(-reaction_x, external_x)
    strain_energy = 0.5 * global_scalar(
        ufl.inner(stress(displacement), strain(displacement)) * ufl.dx, comm
    )
    mean_tip_displacement = global_scalar(displacement[0] * ds(2), comm) / height
    passed = balance_error < 1.0e-8 and strain_energy > 0.0 and mean_tip_displacement > 0.0

    if args.write_fields:
        field_dir = args.output / "elasticity"
        if comm.rank == 0:
            field_dir.mkdir(parents=True, exist_ok=True)
        comm.barrier()
        linear_displacement = fem.Function(
            fem.functionspace(domain, ("Lagrange", 1, (2,))), name="displacement"
        )
        linear_displacement.interpolate(displacement)
        with io.XDMFFile(comm, field_dir / "displacement.xdmf", "w") as xdmf:
            xdmf.write_mesh(domain)
            xdmf.write_function(linear_displacement)

    summary = {
        "example": "linear-elasticity",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(domain),
        "reaction_x": reaction_x,
        "boundary_stress_reaction_x": boundary_reaction_x,
        "applied_force_x": external_x,
        "force_balance_relative_error": balance_error,
        "strain_energy": strain_energy,
        "mean_tip_displacement": mean_tip_displacement,
        "solver_reason": reason,
        "solver_converged": reason > 0,
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError("la placa elástica no satisface balance/energía")


if __name__ == "__main__":
    main()
