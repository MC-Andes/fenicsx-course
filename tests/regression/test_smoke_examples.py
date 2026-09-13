from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("dolfinx")

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.dolfinx
@pytest.mark.parametrize(
    "script,identifier",
    [
        ("00_sanity_check.py", "sanity-check"),
        ("01_poisson_manufactured.py", "poisson-manufactured"),
        ("03_tagged_boundaries.py", "tagged-boundaries"),
        ("04_function_spaces.py", "function-spaces"),
        ("05_heat_diffusion.py", "heat-diffusion"),
        ("06_linear_elasticity.py", "linear-elasticity"),
    ],
)
def test_quick_example(script: str, identifier: str, tmp_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "examples" / script), "--quick", "--output", str(tmp_path)],
        cwd=ROOT,
        check=True,
        timeout=180,
    )
    summary = json.loads((tmp_path / f"{identifier}.json").read_text(encoding="utf-8"))
    assert summary["solver_converged"] is True
    assert summary["validation_passed"] is True


@pytest.mark.dolfinx
def test_quadratic_displacement_can_be_exported(tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "examples/06_linear_elasticity.py"),
            "--quick",
            "--write-fields",
            "--output",
            str(tmp_path),
        ],
        cwd=ROOT,
        check=True,
        timeout=180,
    )
    assert (tmp_path / "elasticity" / "displacement.xdmf").is_file()
    assert (tmp_path / "elasticity" / "displacement.h5").is_file()
