from pathlib import Path

import pytest

from mcandes_fenicsx.metadata import ExampleMetadata, load_metadata


def test_all_example_metadata_is_valid() -> None:
    root = Path(__file__).resolve().parents[2]
    metadata = [load_metadata(path) for path in sorted((root / "examples/metadata").glob("*.yml"))]
    assert len(metadata) >= 10
    assert len({item.identifier for item in metadata}) == len(metadata)
    assert all((root / item.script).is_file() for item in metadata)


def test_metadata_rejects_invalid_identifier() -> None:
    with pytest.raises(ValueError, match="identificador"):
        ExampleMetadata.from_mapping(
            {
                "id": "Bad ID",
                "title": "x",
                "difficulty": "inicial",
                "phenomenon": "x",
                "pde": "x",
                "concepts": [],
                "prerequisites": [],
                "duration_minutes": 1,
                "cost": "x",
                "serial": True,
                "parallel": True,
                "inputs": [],
                "outputs": [],
                "units": "x",
                "command": "x",
                "success": "x",
                "tolerances": {"x": 1.0},
                "sources": ["x"],
                "minimum_version": "0.11",
                "tested_version": "0.11",
                "script": "x.py",
            }
        )
