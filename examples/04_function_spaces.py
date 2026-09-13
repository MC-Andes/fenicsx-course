"""Inspeccionar espacios escalares, vectoriales, tensoriales y mixtos."""

from __future__ import annotations

import dolfinx
from basix.ufl import element, mixed_element
from dolfinx import default_real_type, fem, mesh
from mpi4py import MPI

from mcandes_fenicsx.cli import example_parser
from mcandes_fenicsx.results import emit_result


def global_dofs(space: fem.FunctionSpace) -> int:
    return int(space.dofmap.index_map.size_global * space.dofmap.index_map_bs)


def main() -> None:
    args = example_parser(__doc__).parse_args()
    comm = MPI.COMM_WORLD
    domain = mesh.create_unit_square(comm, 4 if args.quick else 8, 4 if args.quick else 8)
    scalar = fem.functionspace(domain, ("Lagrange", 1))
    vector = fem.functionspace(domain, ("Lagrange", 2, (domain.geometry.dim,)))
    tensor = fem.functionspace(
        domain,
        ("Discontinuous Lagrange", 0, (domain.geometry.dim, domain.geometry.dim)),
    )
    p2 = element(
        "Lagrange",
        domain.basix_cell(),
        2,
        shape=(domain.geometry.dim,),
        dtype=default_real_type,
    )
    p1 = element("Lagrange", domain.basix_cell(), 1, dtype=default_real_type)
    mixed = fem.functionspace(domain, mixed_element([p2, p1]))
    collapsed_pressure, pressure_map = mixed.sub(1).collapse()
    counts = {
        "scalar_p1": global_dofs(scalar),
        "vector_p2": global_dofs(vector),
        "tensor_dg0": global_dofs(tensor),
        "mixed_taylor_hood": global_dofs(mixed),
        "collapsed_pressure": global_dofs(collapsed_pressure),
    }
    passed = (
        counts["vector_p2"] > counts["scalar_p1"]
        and counts["mixed_taylor_hood"] > counts["vector_p2"]
        and len(pressure_map) > 0
    )
    summary = {
        "example": "function-spaces",
        "dolfinx_version": dolfinx.__version__,
        "mpi_size": comm.size,
        "global_dofs": counts,
        "local_pressure_map_size": len(pressure_map),
        "solver_converged": True,
        "validation_passed": passed,
    }
    emit_result(summary, args.output, rank=comm.rank)
    if not passed:
        raise RuntimeError(f"relaciones de grados de libertad inesperadas: {counts}")


if __name__ == "__main__":
    main()
