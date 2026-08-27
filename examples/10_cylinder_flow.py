"""Navier-Stokes estacionario en canal con cilindro mediante Picard."""

from __future__ import annotations

import math

import dolfinx
import numpy as np
import ufl
from basix.ufl import element, mixed_element
from dolfinx import default_real_type, fem, io
from dolfinx.fem.petsc import LinearProblem
from mpi4py import MPI
from petsc4py import PETSc

from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.gmsh_models import channel_with_cylinder
from mcandes_fenicsx.petsc import direct_solver_options
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import (
    global_cell_count,
    global_scalar,
    require_solver_convergence,
)


def main() -> None:
    parser = example_parser(__doc__)
    parser.add_argument("--max-picard", type=int, default=30)
    args = parser.parse_args()
    comm = MPI.COMM_WORLD
    length, height = 2.2, 0.41
    mesh_data = channel_with_cylinder(
        comm,
        length=length,
        height=height,
        mesh_size=0.09 if args.quick else 0.045,
    )
    domain, facet_tags = mesh_data.mesh, mesh_data.facet_tags
    if facet_tags is None:
        raise RuntimeError("Gmsh no produjo etiquetas de frontera")
    ds = ufl.Measure("ds", domain=domain, subdomain_data=facet_tags)
    velocity_element = element(
        "Lagrange", domain.basix_cell(), 2, shape=(2,), dtype=default_real_type
    )
    pressure_element = element("Lagrange", domain.basix_cell(), 1, dtype=default_real_type)
    mixed_space = fem.functionspace(domain, mixed_element([velocity_element, pressure_element]))
    velocity_space, _ = mixed_space.sub(0).collapse()
    previous_velocity = fem.Function(velocity_space, name="picard_velocity")
    peak_velocity = 0.3
    previous_velocity.interpolate(
        lambda x: np.vstack(
            (4.0 * peak_velocity * x[1] * (height - x[1]) / height**2, np.zeros(x.shape[1]))
        )
    )
    inlet_velocity = fem.Function(velocity_space)
    inlet_velocity.interpolate(
        lambda x: np.vstack(
            (4.0 * peak_velocity * x[1] * (height - x[1]) / height**2, np.zeros(x.shape[1]))
        )
    )
    no_slip = fem.Function(velocity_space)
    no_slip.x.array[:] = 0.0
    facet_dim = domain.topology.dim - 1
    inlet_dofs = fem.locate_dofs_topological(
        (mixed_space.sub(0), velocity_space), facet_dim, facet_tags.find(21)
    )
    solid_facets = np.unique(np.hstack((facet_tags.find(23), facet_tags.find(24)))).astype(np.int32)
    solid_dofs = fem.locate_dofs_topological(
        (mixed_space.sub(0), velocity_space), facet_dim, solid_facets
    )
    bcs = [
        fem.dirichletbc(inlet_velocity, inlet_dofs, mixed_space.sub(0)),
        fem.dirichletbc(no_slip, solid_dofs, mixed_space.sub(0)),
    ]
    u, p = ufl.TrialFunctions(mixed_space)
    v, q = ufl.TestFunctions(mixed_space)
    density, viscosity = 1.0, 0.01
    bilinear = (
        viscosity * ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx
        + density * ufl.inner(ufl.dot(previous_velocity, ufl.nabla_grad(u)), v) * ufl.dx
        - ufl.inner(p, ufl.div(v)) * ufl.dx
        + ufl.inner(ufl.div(u), q) * ufl.dx
    )
    zero = fem.Constant(domain, PETSc.ScalarType(0.0))
    linear = zero * (ufl.inner(ufl.as_vector((1.0, 0.0)), v) + q) * ufl.dx
    options = direct_solver_options()
    problem = LinearProblem(
        bilinear,
        linear,
        bcs=bcs,
        petsc_options_prefix="mcandes_cylinder_picard_",
        petsc_options=options,
    )

    tolerance = 2.0e-5 if args.quick else 2.0e-7
    converged = False
    relative_update = math.inf
    solution: fem.Function | None = None
    velocity: fem.Function | None = None
    pressure: fem.Function | None = None
    iteration = 0
    for _ in range(args.max_picard):
        iteration += 1
        solution = problem.solve()
        reason = require_solver_convergence(problem.solver, "cilindro KSP")
        velocity = solution.sub(0).collapse()
        pressure = solution.sub(1).collapse()
        velocity.x.scatter_forward()
        owned = velocity_space.dofmap.index_map.size_local * velocity_space.dofmap.index_map_bs
        difference = velocity.x.array[:owned] - previous_velocity.x.array[:owned]
        local_difference = float(np.vdot(difference, difference).real)
        local_norm = float(np.vdot(velocity.x.array[:owned], velocity.x.array[:owned]).real)
        difference_norm = math.sqrt(comm.allreduce(local_difference, op=MPI.SUM))
        velocity_norm = math.sqrt(comm.allreduce(local_norm, op=MPI.SUM))
        relative_update = difference_norm / max(velocity_norm, 1.0e-15)
        previous_velocity.x.array[:] = velocity.x.array
        previous_velocity.x.scatter_forward()
        if relative_update < tolerance:
            converged = True
            break
    assert solution is not None and velocity is not None and pressure is not None
    velocity.name, pressure.name = "velocity", "pressure"
    normal = ufl.FacetNormal(domain)
    stress = -pressure * ufl.Identity(2) + viscosity * (
        ufl.grad(velocity) + ufl.grad(velocity).T
    )
    drag = global_scalar(ufl.dot(stress, normal)[0] * ds(24), comm)
    inlet_flux = -global_scalar(ufl.dot(velocity, normal) * ds(21), comm)
    outlet_flux = global_scalar(ufl.dot(velocity, normal) * ds(22), comm)
    mass_balance_error = abs(outlet_flux - inlet_flux) / max(abs(inlet_flux), 1.0e-15)
    passed = converged and mass_balance_error < 4.0e-2 and abs(drag) > 1.0e-6

    if args.write_fields:
        field_dir = args.output / "cylinder"
        if comm.rank == 0:
            field_dir.mkdir(parents=True, exist_ok=True)
        comm.barrier()
        with io.XDMFFile(comm, field_dir / "velocity.xdmf", "w") as xdmf:
            xdmf.write_mesh(domain)
            linear_velocity = fem.Function(
                fem.functionspace(domain, ("Lagrange", 1, (2,))), name="velocity"
            )
            linear_velocity.interpolate(velocity)
            xdmf.write_function(linear_velocity)
        with io.XDMFFile(comm, field_dir / "pressure.xdmf", "w") as xdmf:
            xdmf.write_mesh(domain)
            xdmf.write_function(pressure)

    summary = {
        "example": "cylinder-flow",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(domain),
        "reynolds_number": density * peak_velocity * (2.0 * 0.05) / viscosity,
        "picard_iterations": iteration,
        "picard_relative_update": relative_update,
        "drag_force_x": drag,
        "inlet_flux": inlet_flux,
        "outlet_flux": outlet_flux,
        "mass_balance_relative_error": mass_balance_error,
        "solver_reason": reason,
        "solver_converged": converged,
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError("el flujo con cilindro no satisfizo Picard/balance")


if __name__ == "__main__":
    main()
