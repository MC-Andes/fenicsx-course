"""Carga y validación de las fichas estructuradas de los ejemplos."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

_IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_DIFFICULTIES = {"inicial", "intermedio", "avanzado", "integrador"}


@dataclass(frozen=True)
class ExampleMetadata:
    """Contrato mínimo que una demostración publicable debe cumplir."""

    identifier: str
    title: str
    difficulty: str
    phenomenon: str
    pde: str
    concepts: tuple[str, ...]
    prerequisites: tuple[str, ...]
    duration_minutes: int
    cost: str
    serial: bool
    parallel: bool
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    units: str
    command: str
    success: str
    tolerances: dict[str, float]
    sources: tuple[str, ...]
    seed: int | None
    minimum_version: str
    tested_version: str
    script: str

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> ExampleMetadata:
        """Construir una ficha y fallar temprano ante datos ambiguos."""

        required = {
            "id",
            "title",
            "difficulty",
            "phenomenon",
            "pde",
            "concepts",
            "prerequisites",
            "duration_minutes",
            "cost",
            "serial",
            "parallel",
            "inputs",
            "outputs",
            "units",
            "command",
            "success",
            "tolerances",
            "sources",
            "minimum_version",
            "tested_version",
            "script",
        }
        missing = sorted(required - data.keys())
        if missing:
            raise ValueError(f"faltan campos obligatorios: {', '.join(missing)}")

        identifier = str(data["id"])
        if not _IDENTIFIER.fullmatch(identifier):
            raise ValueError(f"identificador no válido: {identifier!r}")
        difficulty = str(data["difficulty"]).lower()
        if difficulty not in _DIFFICULTIES:
            raise ValueError(f"dificultad no válida: {difficulty!r}")
        duration = int(data["duration_minutes"])
        if duration <= 0:
            raise ValueError("duration_minutes debe ser positivo")
        tolerances = {str(key): float(value) for key, value in dict(data["tolerances"]).items()}
        if not tolerances or any(value <= 0 for value in tolerances.values()):
            raise ValueError("tolerances debe contener valores positivos")
        sources = tuple(str(item) for item in data["sources"])
        if not sources:
            raise ValueError("cada ejemplo debe declarar al menos una fuente")

        return cls(
            identifier=identifier,
            title=str(data["title"]),
            difficulty=difficulty,
            phenomenon=str(data["phenomenon"]),
            pde=str(data["pde"]),
            concepts=tuple(str(item) for item in data["concepts"]),
            prerequisites=tuple(str(item) for item in data["prerequisites"]),
            duration_minutes=duration,
            cost=str(data["cost"]),
            serial=bool(data["serial"]),
            parallel=bool(data["parallel"]),
            inputs=tuple(str(item) for item in data["inputs"]),
            outputs=tuple(str(item) for item in data["outputs"]),
            units=str(data["units"]),
            command=str(data["command"]),
            success=str(data["success"]),
            tolerances=tolerances,
            sources=sources,
            seed=int(data["seed"]) if data.get("seed") is not None else None,
            minimum_version=str(data["minimum_version"]),
            tested_version=str(data["tested_version"]),
            script=str(data["script"]),
        )


def load_metadata(path: str | Path) -> ExampleMetadata:
    """Leer una ficha YAML segura."""

    metadata_path = Path(path)
    data = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{metadata_path} no contiene un objeto YAML")
    return ExampleMetadata.from_mapping(data)
