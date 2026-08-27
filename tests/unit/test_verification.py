import math

import pytest

from mcandes_fenicsx.verification import convergence_rates, relative_difference


def test_convergence_rates_nonuniform_meshes() -> None:
    sizes = [0.5, 0.25, 0.1]
    errors = [size**2 for size in sizes]
    assert convergence_rates(sizes, errors) == pytest.approx([2.0, 2.0])


def test_convergence_rates_reject_bad_input() -> None:
    with pytest.raises(ValueError):
        convergence_rates([1.0], [1.0])
    with pytest.raises(ValueError):
        convergence_rates([1.0, 1.0], [1.0, 0.5])


def test_relative_difference() -> None:
    assert relative_difference(1.01, 1.0) == pytest.approx(0.01)
    assert math.isfinite(relative_difference(0.0, 0.0))
