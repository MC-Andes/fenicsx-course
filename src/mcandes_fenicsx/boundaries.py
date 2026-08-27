"""Etiquetas de frontera para geometrías rectangulares incorporadas."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np


def tag_boundaries(mesh: Any, locators: dict[int, Callable[[np.ndarray], np.ndarray]]) -> Any:
    """Crear MeshTags ordenadas; una faceta no debe pertenecer a dos etiquetas."""

    from dolfinx import mesh as dmesh

    facet_dim = mesh.topology.dim - 1
    indices: list[np.ndarray] = []
    values: list[np.ndarray] = []
    for marker, locator in locators.items():
        facets = dmesh.locate_entities_boundary(mesh, facet_dim, locator)
        indices.append(facets)
        values.append(np.full(facets.shape, marker, dtype=np.int32))
    all_indices = np.hstack(indices).astype(np.int32)
    all_values = np.hstack(values).astype(np.int32)
    if np.unique(all_indices).size != all_indices.size:
        raise ValueError("una faceta fue asignada a más de una etiqueta")
    order = np.argsort(all_indices)
    return dmesh.meshtags(mesh, facet_dim, all_indices[order], all_values[order])
