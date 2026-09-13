"""Stokes Taylor-Hood manufacturado: Poiseuille, presión y balance de flujo."""

from __future__ import annotations

import math

import dolfinx
import numpy as np
import ufl
from basix.ufl import element
from dolfinx import default_real_type, fem, mesh
from dolfinx.fem.petsc import LinearProblem, create_vector
from mpi4py import MPI
from petsc4py import PETSc

from mcandes_fenicsx.boundaries import tag_boundaries
from mcandes_fenicsx.cli import example_parser
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
    n = 10 if args.quick else 24
    domain = mesh.create_rectangle(
        comm,
        [np.array([0.0, 0.0]), np.array([1.0, 1.0])],
        (2 * n, n),
        cell_type=mesh.CellType.triangle,
    )
    facet_tags = tag_boundaries(
        domain,
        {
            1: lambda x: np.isclose(x[0], 0.0),
            2: lambda x: np.isclose(x[0], 1.0),
            3: lambda x: np.isclose(x[1], 0.0),
            4: lambda x: np.isclose(x[1], 1.0),
        },
    )
    ds = ufl.Measure("ds", domain=domain, subdomain_data=facet_tags)
    p2 = element("Lagrange", domain.basix_cell(), 2, shape=(2,), dtype=default_real_type)
    p1 = element("Lagrange", domain.basix_cell(), 1, dtype=default_real_type)
    velocity_space, pressure_space = fem.functionspace(domain, p2), fem.functionspace(domain, p1)
    velocity_exact = fem.Function(velocity_space, name="poiseuille_exact")
    velocity_exact.interpolate(
        lambda x: np.vstack((4.0 * x[1] * (1.0 - x[1]), np.zeros(x.shape[1])))
    )
    all_facets = mesh.locate_entities_boundary(
        domain, domain.topology.dim - 1, lambda x: np.full(x.shape[1], True)
    )
    velocity_dofs = fem.locate_dofs_topological(
        velocity_space, domain.topology.dim - 1, all_facets
    )
    velocity_bc = fem.dirichletbc(velocity_exact, velocity_dofs)
    u, p = ufl.TrialFunction(velocity_space), ufl.TrialFunction(pressure_space)
    v, q = ufl.TestFunction(velocity_space), ufl.TestFunction(pressure_space)
    zero = fem.Constant(domain, PETSc.ScalarType(0.0))
    bilinear = [
        [ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx, -ufl.inner(p, ufl.div(v)) * ufl.dx],
        [-ufl.inner(ufl.div(u), q) * ufl.dx, None],
    ]
    linear = [ufl.inner(ufl.as_vector((zero, zero)), v) * ufl.dx, zero * q * ufl.dx]
    preconditioner = [
        [bilinear[0][0], None],
        [None, ufl.inner(p, q) * ufl.dx],
    ]
    problem = LinearProblem(
        bilinear,
        linear,
        P=preconditioner,
        bcs=[velocity_bc],
        kind="nest",
        petsc_options_prefix="mcandes_stokes_",
        petsc_options={
            "ksp_type": "minres",
            "ksp_rtol": 1.0e-10,
            "ksp_error_if_not_converged": True,
            "pc_type": "fieldsplit",
            "pc_fieldsplit_type": "additive",
            "fieldsplit_0_ksp_type": "preonly",
            "fieldsplit_0_pc_type": "gamg",
            "fieldsplit_1_ksp_type": "preonly",
            "fieldsplit_1_pc_type": "jacobi",
        },
    )
    null_vector = create_vector([velocity_space, pressure_space], "nest")
    velocity_null, pressure_null = null_vector.getNestSubVecs()
    velocity_null.set(0.0)
    pressure_null.set(1.0)
    null_vector.normalize()
    nullspace = PETSc.NullSpace().create(vectors=[null_vector])
    problem.A.setNullSpace(nullspace)
    velocity, pressure = problem.solve()
    velocity.name, pressure.name = "velocity", "pressure"
    velocity.x.scatter_forward()
    pressure.x.scatter_forward()
    reason = require_solver_convergence(problem.solver, "Stokes KSP")

    area = global_scalar(1.0 * ufl.dx(domain=domain), comm)
    pressure_mean = global_scalar(pressure * ufl.dx, comm) / area
    pressure.x.array[:] -= PETSc.ScalarType(pressure_mean)
    pressure.x.scatter_forward()
    x = ufl.SpatialCoordinate(domain)
    exact_velocity = ufl.as_vector((4.0 * x[1] * (1.0 - x[1]), 0.0))
    exact_pressure = 4.0 - 8.0 * x[0]
    velocity_error = global_l2_error(velocity, exact_velocity)
    pressure_error = global_l2_error(pressure, exact_pressure)
    divergence_squared = global_scalar(ufl.div(velocity) ** 2 * ufl.dx, comm)
    divergence_norm = math.sqrt(max(divergence_squared, 0.0))
    flow_rate = global_scalar(velocity[0] * ds(2), comm)
    flow_error = abs(flow_rate - 2.0 / 3.0)
    passed = (
        velocity_error < 2.0e-6
        and pressure_error < 2.0e-5
        and divergence_norm < 2.0e-6
        and flow_error < 2.0e-6
    )
    summary = {
        "example": "stokes-channel",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(domain),
        "velocity_l2_error": velocity_error,
        "pressure_l2_error": pressure_error,
        "divergence_l2": divergence_norm,
        "flow_rate": flow_rate,
        "flow_rate_error": flow_error,
        "solver_reason": reason,
        "solver_converged": reason > 0,
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError("Stokes no reprodujo la solución manufacturada")


if __name__ == "__main__":
    main()
