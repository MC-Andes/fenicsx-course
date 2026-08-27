"""Bloque neo-Hookeano con carga incremental y comprobación de Jacobiano."""

from __future__ import annotations

import dolfinx
import numpy as np
import ufl
from dolfinx import fem, io, mesh
from dolfinx.fem.petsc import NonlinearProblem
from mpi4py import MPI
from petsc4py import PETSc

from mcandes_fenicsx.boundaries import tag_boundaries
from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.petsc import nonlinear_solver_options
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import (
    global_cell_count,
    global_scalar,
    require_solver_convergence,
)


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    length, height = 1.0, 0.2
    domain = mesh.create_rectangle(
        comm,
        [np.array([0.0, 0.0]), np.array([length, height])],
        (20 if args.quick else 50, 4 if args.quick else 10),
        cell_type=mesh.CellType.triangle,
    )
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
    space = fem.functionspace(domain, ("Lagrange", 2, (2,)))
    displacement = fem.Function(space, name="displacement")
    test = ufl.TestFunction(space)
    left_dofs = fem.locate_dofs_topological(
        space, domain.topology.dim - 1, facet_tags.find(1)
    )
    bc = fem.dirichletbc(np.zeros(2, dtype=PETSc.ScalarType), left_dofs, space)
    young, poisson = 100.0, 0.3
    mu = young / (2.0 * (1.0 + poisson))
    lame = young * poisson / ((1.0 + poisson) * (1.0 - 2.0 * poisson))
    identity = ufl.Identity(2)
    deformation_gradient = ufl.variable(identity + ufl.grad(displacement))
    right_cauchy_green = deformation_gradient.T * deformation_gradient
    jacobian = ufl.det(deformation_gradient)
    log_j = ufl.ln(jacobian)
    energy_density = (
        0.5 * mu * (ufl.tr(right_cauchy_green) - 2.0)
        - mu * log_j
        + 0.5 * lame * log_j**2
    )
    traction = fem.Constant(domain, (PETSc.ScalarType(0.0), PETSc.ScalarType(0.0)))
    potential = energy_density * ufl.dx - ufl.dot(traction, displacement) * ds(2)
    residual = ufl.derivative(potential, displacement, test)
    problem = NonlinearProblem(
        residual,
        displacement,
        bcs=[bc],
        petsc_options_prefix="mcandes_hyperelastic_",
        petsc_options=nonlinear_solver_options(),
    )
    final_load = 5.0
    loads = np.linspace(final_load / (3 if args.quick else 6), final_load, 3 if args.quick else 6)
    reasons: list[int] = []
    iterations: list[int] = []
    for load in loads:
        traction.value[0] = PETSc.ScalarType(load)
        problem.solve()
        displacement.x.scatter_forward()
        reasons.append(require_solver_convergence(problem.solver, "hiperelasticidad SNES"))
        iterations.append(int(problem.solver.getIterationNumber()))

    dg0 = fem.functionspace(domain, ("Discontinuous Lagrange", 0))
    jacobian_field = fem.Function(dg0, name="J")
    jacobian_field.interpolate(fem.Expression(jacobian, dg0.element.interpolation_points))
    owned = dg0.dofmap.index_map.size_local
    local_min = float(np.min(jacobian_field.x.array[:owned])) if owned else float("inf")
    minimum_jacobian = float(comm.allreduce(local_min, op=MPI.MIN))
    strain_energy = global_scalar(energy_density * ufl.dx, comm)
    first_piola = ufl.diff(energy_density, deformation_gradient)
    boundary_reaction = global_scalar(
        ufl.dot(first_piola, ufl.FacetNormal(domain))[0] * ds(1), comm
    )
    virtual_left_translation = fem.Function(space)
    virtual_left_translation.interpolate(
        lambda x: np.vstack((np.isclose(x[0], 0.0).astype(float), np.zeros(x.shape[1])))
    )
    reaction = global_scalar(
        ufl.derivative(potential, displacement, virtual_left_translation), comm
    )
    balance_error = abs(reaction + final_load * height) / (final_load * height)
    mean_tip = global_scalar(displacement[0] * ds(2), comm) / height
    passed = (
        all(reason > 0 for reason in reasons)
        and minimum_jacobian > 0.5
        and strain_energy > 0.0
        and balance_error < 2.0e-6
        and mean_tip > 0.0
    )

    if args.write_fields:
        field_dir = args.output / "hyperelasticity"
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
        with io.XDMFFile(comm, field_dir / "jacobian.xdmf", "w") as xdmf:
            xdmf.write_mesh(domain)
            xdmf.write_function(jacobian_field)

    summary = {
        "example": "hyperelasticity",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(domain),
        "load_steps": len(loads),
        "snes_iterations": iterations,
        "minimum_jacobian": minimum_jacobian,
        "strain_energy": strain_energy,
        "reaction_x": reaction,
        "boundary_stress_reaction_x": boundary_reaction,
        "force_balance_relative_error": balance_error,
        "mean_tip_displacement": mean_tip,
        "solver_converged": all(reason > 0 for reason in reasons),
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError("la solución hiperelástica no pasó sus invariantes")


if __name__ == "__main__":
    main()
