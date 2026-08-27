"""Placa de dos materiales: etiquetas de celda, continuidad y balance."""

from __future__ import annotations

import math

import dolfinx
import numpy as np
import ufl
from dolfinx import fem, mesh
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
    require_solver_convergence,
)


def lame_parameters(young: float, poisson: float) -> tuple[float, float]:
    mu = young / (2.0 * (1.0 + poisson))
    lambda_ps = young * poisson / (1.0 - poisson**2)
    return mu, lambda_ps


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    length, height = 2.0, 1.0
    nx, ny = (20, 10) if args.quick else (60, 30)
    domain = mesh.create_rectangle(
        comm,
        [np.array([0.0, 0.0]), np.array([length, height])],
        (nx, ny),
        cell_type=mesh.CellType.triangle,
    )
    tdim = domain.topology.dim
    cell_map = domain.topology.index_map(tdim)
    cells = np.arange(cell_map.size_local, dtype=np.int32)
    midpoints = mesh.compute_midpoints(domain, tdim, cells)
    material_values = np.where(midpoints[:, 0] < length / 2.0, 1, 2).astype(np.int32)
    cell_tags = mesh.meshtags(domain, tdim, cells, material_values)
    dx = ufl.Measure("dx", domain=domain, subdomain_data=cell_tags)
    facet_tags = tag_boundaries(
        domain,
        {
            1: lambda x: np.isclose(x[0], 0.0),
            2: lambda x: np.isclose(x[0], length),
            3: lambda x: np.isclose(x[1], 0.0),
            4: lambda x: np.isclose(x[1], height),
        },
    )
    ds = ufl.Measure("ds", domain=domain, subdomain_data=facet_tags)
    space = fem.functionspace(domain, ("Lagrange", 1, (2,)))
    trial, test = ufl.TrialFunction(space), ufl.TestFunction(space)

    def strain(displacement: ufl.core.expr.Expr) -> ufl.core.expr.Expr:
        return ufl.sym(ufl.grad(displacement))

    def stress(displacement: ufl.core.expr.Expr, young: float) -> ufl.core.expr.Expr:
        mu, lambda_ps = lame_parameters(young, 0.3)
        return 2.0 * mu * strain(displacement) + lambda_ps * ufl.tr(strain(displacement)) * ufl.Identity(2)

    bilinear = sum(
        ufl.inner(stress(trial, young), strain(test)) * dx(marker)
        for marker, young in ((1, 100.0), (2, 400.0))
    )
    traction = fem.Constant(domain, (PETSc.ScalarType(1.0), PETSc.ScalarType(0.0)))
    left_dofs = fem.locate_dofs_topological(space, tdim - 1, facet_tags.find(1))
    bc = fem.dirichletbc(np.zeros(2, dtype=PETSc.ScalarType), left_dofs, space)
    problem = LinearProblem(
        bilinear,
        ufl.inner(traction, test) * ds(2),
        bcs=[bc],
        petsc_options_prefix="mcandes_two_materials_",
        petsc_options=direct_solver_options(),
    )
    displacement = problem.solve()
    displacement.x.scatter_forward()
    reason = require_solver_convergence(problem.solver, "dos materiales KSP")
    normal = ufl.FacetNormal(domain)
    boundary_reaction = global_scalar(
        ufl.dot(stress(displacement, 100.0), normal)[0] * ds(1), comm
    )
    virtual_left_translation = fem.Function(space)
    virtual_left_translation.interpolate(
        lambda x: np.vstack((np.isclose(x[0], 0.0).astype(float), np.zeros(x.shape[1])))
    )
    reaction = global_scalar(
        sum(
            ufl.inner(stress(displacement, young), strain(virtual_left_translation)) * dx(marker)
            for marker, young in ((1, 100.0), (2, 400.0))
        )
        - ufl.inner(traction, virtual_left_translation) * ds(2),
        comm,
    )
    balance_error = abs(reaction + height) / height
    jump_squared = global_scalar(ufl.inner(ufl.jump(displacement), ufl.jump(displacement)) * ufl.dS, comm)
    jump_norm = math.sqrt(max(jump_squared, 0.0))
    mean_tip = global_scalar(displacement[0] * ds(2), comm) / height
    passed = balance_error < 1.0e-8 and jump_norm < 1.0e-10 and mean_tip > 0.0
    summary = {
        "example": "two-materials",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(domain),
        "force_balance_relative_error": balance_error,
        "boundary_stress_reaction_x": boundary_reaction,
        "displacement_jump_l2": jump_norm,
        "mean_tip_displacement": mean_tip,
        "solver_reason": reason,
        "solver_converged": reason > 0,
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError("continuidad o balance de la placa bimaterial falló")


if __name__ == "__main__":
    main()
