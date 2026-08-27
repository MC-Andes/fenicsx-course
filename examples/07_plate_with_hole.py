"""Placa con agujero Gmsh y factor de concentración de von Mises."""

from __future__ import annotations

import dolfinx
import numpy as np
import ufl
from dolfinx import fem, io
from dolfinx.fem.petsc import LinearProblem
from mpi4py import MPI
from petsc4py import PETSc

from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.gmsh_models import rectangle_with_hole
from mcandes_fenicsx.petsc import direct_solver_options
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import (
    global_cell_count,
    global_scalar,
    require_solver_convergence,
)


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    length, height, radius = 2.0, 1.0, 0.2
    mesh_data = rectangle_with_hole(
        comm,
        length=length,
        height=height,
        radius=radius,
        mesh_size=0.12 if args.quick else 0.055,
    )
    domain, facet_tags = mesh_data.mesh, mesh_data.facet_tags
    if facet_tags is None:
        raise RuntimeError("Gmsh no produjo etiquetas de faceta")
    ds = ufl.Measure("ds", domain=domain, subdomain_data=facet_tags)
    space = fem.functionspace(domain, ("Lagrange", 2, (2,)))
    trial, test = ufl.TrialFunction(space), ufl.TestFunction(space)
    young, poisson = 100.0, 0.3
    mu = young / (2.0 * (1.0 + poisson))
    lambda_ps = young * poisson / (1.0 - poisson**2)

    def strain(displacement: ufl.core.expr.Expr) -> ufl.core.expr.Expr:
        return ufl.sym(ufl.grad(displacement))

    def stress(displacement: ufl.core.expr.Expr) -> ufl.core.expr.Expr:
        return 2.0 * mu * strain(displacement) + lambda_ps * ufl.tr(strain(displacement)) * ufl.Identity(2)

    traction_value = 1.0
    traction = fem.Constant(domain, (PETSc.ScalarType(traction_value), PETSc.ScalarType(0.0)))
    left_dofs = fem.locate_dofs_topological(space, domain.topology.dim - 1, facet_tags.find(11))
    bc = fem.dirichletbc(np.zeros(2, dtype=PETSc.ScalarType), left_dofs, space)
    problem = LinearProblem(
        ufl.inner(stress(trial), strain(test)) * ufl.dx,
        ufl.inner(traction, test) * ds(12),
        bcs=[bc],
        petsc_options_prefix="mcandes_plate_hole_",
        petsc_options=direct_solver_options(),
    )
    displacement = problem.solve()
    displacement.name = "displacement"
    displacement.x.scatter_forward()
    reason = require_solver_convergence(problem.solver, "placa con agujero KSP")

    sigma = stress(displacement)
    von_mises = ufl.sqrt(sigma[0, 0] ** 2 - sigma[0, 0] * sigma[1, 1] + sigma[1, 1] ** 2 + 3.0 * sigma[0, 1] ** 2)
    dg0 = fem.functionspace(domain, ("Discontinuous Lagrange", 0))
    vm_field = fem.Function(dg0, name="von_mises")
    vm_field.interpolate(fem.Expression(von_mises, dg0.element.interpolation_points))
    owned = dg0.dofmap.index_map.size_local
    coordinates = dg0.tabulate_dof_coordinates()[:owned]
    distance = np.sqrt((coordinates[:, 0] - length / 2.0) ** 2 + coordinates[:, 1] ** 2)
    near_hole = vm_field.x.array[:owned][distance < radius + 0.18]
    local_max = float(np.max(near_hole)) if near_hole.size else 0.0
    stress_max = float(comm.allreduce(local_max, op=MPI.MAX))
    concentration = stress_max / traction_value
    boundary_reaction = global_scalar(
        ufl.dot(sigma, ufl.FacetNormal(domain))[0] * ds(11), comm
    )
    virtual_left_translation = fem.Function(space)
    virtual_left_translation.interpolate(
        lambda x: np.vstack((np.isclose(x[0], 0.0).astype(float), np.zeros(x.shape[1])))
    )
    reaction = global_scalar(
        ufl.inner(stress(displacement), strain(virtual_left_translation)) * ufl.dx
        - ufl.inner(traction, virtual_left_translation) * ds(12),
        comm,
    )
    applied = traction_value * height
    balance_error = abs(reaction + applied) / applied
    passed = 1.5 < concentration < 8.0 and balance_error < 2.0e-7

    if args.write_fields:
        field_dir = args.output / "plate-with-hole"
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
        with io.XDMFFile(comm, field_dir / "von_mises.xdmf", "w") as xdmf:
            xdmf.write_mesh(domain)
            xdmf.write_function(vm_field)

    summary = {
        "example": "plate-with-hole",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(domain),
        "stress_concentration_factor": concentration,
        "reaction_x": reaction,
        "boundary_stress_reaction_x": boundary_reaction,
        "force_balance_relative_error": balance_error,
        "solver_reason": reason,
        "solver_converged": reason > 0,
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError("concentración o balance fuera de tolerancia")


if __name__ == "__main__":
    main()
