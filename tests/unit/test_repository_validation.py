from pathlib import Path

from mcandes_fenicsx.validation_cli import validate_repository


def test_repository_contract() -> None:
    root = Path(__file__).resolve().parents[2]
    assert validate_repository(root) == []


def test_catalog_contains_only_local_verifiable_examples() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "docs" / "all-fem").exists()
    for path in (root / "examples" / "metadata").glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        assert "all_fem_id" not in text
        assert "doi.org/10.1016/j.cma.2026.118985" not in text
