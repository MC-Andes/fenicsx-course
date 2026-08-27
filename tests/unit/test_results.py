import json

import pytest

from mcandes_fenicsx.results import emit_result


def test_emit_result_writes_only_root(tmp_path) -> None:
    summary = {
        "example": "unit-example",
        "dolfinx_version": "0.11.0.post0",
        "mpi_size": 2,
        "solver_converged": True,
        "validation_passed": True,
        "metric": 1.25,
    }
    assert emit_result(summary, tmp_path, rank=1, print_json=False) is None
    path = emit_result(summary, tmp_path, rank=0, print_json=False)
    assert path is not None
    assert json.loads(path.read_text(encoding="utf-8"))["metric"] == 1.25


def test_emit_result_rejects_non_finite(tmp_path) -> None:
    with pytest.raises(ValueError, match="NaN"):
        emit_result(
            {
                "example": "bad",
                "dolfinx_version": "x",
                "mpi_size": 1,
                "solver_converged": True,
                "validation_passed": False,
                "metric": float("nan"),
            },
            tmp_path,
            print_json=False,
        )
