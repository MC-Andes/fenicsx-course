"""Cahn-Hilliard mixto: masa conservada y energía libre no creciente."""

from __future__ import annotations

import dolfinx
import numpy as np
import ufl
from basix.ufl import element, mixed_element
from dolfinx import default_real_type, fem, io, mesh
from dolfinx.fem.petsc import NonlinearProblem
from mpi4py import MPI

from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import (
    global_cell_count,
    global_scalar,
    require_solver_convergence,
)


def free_energy(concentration: ufl.core.expr.Expr, surface: float) -> ufl.core.expr.Expr:
    bulk = 100.0 * concentration**2 * (1.0 - concentration) ** 2
    interface = 0.5 * surface * ufl.inner(ufl.grad(concentration), ufl.grad(concentration))
    return bulk + interface


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    n = 16 if args.quick else 32
    steps = 3 if args.quick else 12
    time_step = 5.0e-6
    surface = 1.0e-2
    domain = mesh.create_unit_square(comm, n, n, mesh.CellType.triangle)
    p1 = element("Lagrange", domain.basix_cell(), 1, dtype=default_real_type)
    mixed_space = fem.functionspace(domain, mixed_element([p1, p1]))
    q, v = ufl.TestFunctions(mixed_space)
    current = fem.Function(mixed_space, name="state")
    previous = fem.Function(mixed_space, name="previous_state")
    current.sub(0).interpolate(
        lambda x: 0.63 + 0.02 * np.cos(2.0 * np.pi * x[0]) * np.cos(2.0 * np.pi * x[1])
    )
    current.x.scatter_forward()
    previous.x.array[:] = current.x.array
    previous.x.scatter_forward()
    concentration, chemical_potential = ufl.split(current)
    concentration_previous, _ = ufl.split(previous)
    concentration_variable = ufl.variable(concentration)
    bulk = 100.0 * concentration_variable**2 * (1.0 - concentration_variable) ** 2
    derivative_bulk = ufl.diff(bulk, concentration_variable)
    residual_mass = (
        ufl.inner(concentration - concentration_previous, q) * ufl.dx
        + time_step * ufl.inner(ufl.grad(chemical_potential), ufl.grad(q)) * ufl.dx
    )
    residual_chemical = (
        ufl.inner(chemical_potential, v) * ufl.dx
        - ufl.inner(derivative_bulk, v) * ufl.dx
        - surface * ufl.inner(ufl.grad(concentration), ufl.grad(v)) * ufl.dx
    )
    cahn_hilliard_options = {
        "snes_type": "newtonls",
        "snes_linesearch_type": "none",
        "snes_stol": np.sqrt(np.finfo(default_real_type).eps) * 1.0e-2,
        "snes_atol": 0.0,
        "snes_rtol": 0.0,
        "snes_max_it": 40,
        "snes_error_if_not_converged": True,
        "ksp_type": "preonly",
        "pc_type": "lu",
        "ksp_error_if_not_converged": True,
    }
    problem = NonlinearProblem(
        residual_mass + residual_chemical,
        current,
        petsc_options_prefix="mcandes_cahn_hilliard_",
        petsc_options=cahn_hilliard_options,
    )
    initial_concentration = current.sub(0).collapse()
    initial_mass = global_scalar(initial_concentration * ufl.dx, comm)
    masses = [initial_mass]
    energies = [global_scalar(free_energy(initial_concentration, surface) * ufl.dx, comm)]
    reasons: list[int] = []
    iterations: list[int] = []
    for _ in range(steps):
        problem.solve()
        current.x.scatter_forward()
        reasons.append(require_solver_convergence(problem.solver, "Cahn-Hilliard SNES"))
        iterations.append(int(problem.solver.getIterationNumber()))
        concentration_field = current.sub(0).collapse()
        concentration_field.x.scatter_forward()
        masses.append(global_scalar(concentration_field * ufl.dx, comm))
        energies.append(global_scalar(free_energy(concentration_field, surface) * ufl.dx, comm))
        previous.x.array[:] = current.x.array
        previous.x.scatter_forward()

    mass_drift = max(abs(value - initial_mass) for value in masses)
    energy_increases = [
        energies[index] - energies[index - 1] for index in range(1, len(energies))
    ]
    max_energy_increase = max(energy_increases)
    passed = (
        all(reason > 0 for reason in reasons)
        and mass_drift < 1.0e-9
        and max_energy_increase < 1.0e-8
    )
    final_concentration = current.sub(0).collapse()
    final_concentration.name = "concentration"

    if args.write_fields:
        field_dir = args.output / "cahn-hilliard"
        if comm.rank == 0:
            field_dir.mkdir(parents=True, exist_ok=True)
        comm.barrier()
        with io.XDMFFile(comm, field_dir / "concentration.xdmf", "w") as xdmf:
            xdmf.write_mesh(domain)
            xdmf.write_function(final_concentration, steps * time_step)

    summary = {
        "example": "cahn-hilliard",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "mesh_cells_global": global_cell_count(domain),
        "time_steps": steps,
        "masses": masses,
        "mass_drift": mass_drift,
        "free_energies": energies,
        "maximum_energy_increase": max_energy_increase,
        "snes_iterations": iterations,
        "solver_converged": all(reason > 0 for reason in reasons),
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError("Cahn-Hilliard perdió masa o incrementó la energía")


if __name__ == "__main__":
    main()
