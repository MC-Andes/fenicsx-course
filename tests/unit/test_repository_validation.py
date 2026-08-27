from pathlib import Path

from mcandes_fenicsx.validation_cli import validate_repository


def test_repository_contract() -> None:
    root = Path(__file__).resolve().parents[2]
    assert validate_repository(root) == []
