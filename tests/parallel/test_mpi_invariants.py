from __future__ import annotations

import pytest

from mcandes_fenicsx.verification import global_cell_count

mesh = pytest.importorskip("dolfinx.mesh")
MPI = pytest.importorskip("mpi4py").MPI


@pytest.mark.parallel
def test_global_cell_count_with_two_ranks() -> None:
    if MPI.COMM_WORLD.size != 2:
        pytest.skip("ejecute con mpirun -n 2")
    domain = mesh.create_unit_square(MPI.COMM_WORLD, 4, 3)
    assert global_cell_count(domain) == 24
