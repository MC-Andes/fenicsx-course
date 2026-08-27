"""Geometrías Gmsh originales del curso y sus grupos físicos."""

from __future__ import annotations

from typing import Any


def _classify_rectangle_with_circle(
    model: Any,
    boundary: list[tuple[int, int]],
    *,
    length: float,
    y_min: float,
    y_max: float,
    circle_center: tuple[float, float],
    radius: float,
) -> dict[str, list[int]]:
    groups: dict[str, list[int]] = {"left": [], "right": [], "walls": [], "circle": []}
    tolerance = max(length, y_max - y_min) * 1.0e-6
    cx, cy = circle_center
    for _, tag in boundary:
        xmin, ymin, _, xmax, ymax, _ = model.getBoundingBox(1, tag)
        if abs(xmin) < tolerance and abs(xmax) < tolerance:
            groups["left"].append(tag)
        elif abs(xmin - length) < tolerance and abs(xmax - length) < tolerance:
            groups["right"].append(tag)
        elif (
            abs(xmin - (cx - radius)) < tolerance
            and abs(xmax - (cx + radius)) < tolerance
            and abs(ymin - (cy - radius)) < tolerance
            and abs(ymax - (cy + radius)) < tolerance
        ):
            groups["circle"].append(tag)
        else:
            groups["walls"].append(tag)
    if any(not entries for entries in groups.values()):
        raise RuntimeError(f"no se pudieron clasificar todas las fronteras Gmsh: {groups}")
    return groups


def rectangle_with_hole(
    comm: Any,
    *,
    length: float = 2.0,
    height: float = 1.0,
    radius: float = 0.2,
    mesh_size: float = 0.08,
) -> Any:
    """Placa 2D con agujero, grupos 1/11/12/13/14 (dominio/fronteras)."""

    import gmsh
    from dolfinx.io import gmsh as gmshio

    y_min, y_max = -height / 2.0, height / 2.0
    center = (length / 2.0, 0.0)
    if comm.rank == 0:
        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("plate-with-hole")
        rectangle = gmsh.model.occ.addRectangle(0.0, y_min, 0.0, length, height)
        disk = gmsh.model.occ.addDisk(center[0], center[1], 0.0, radius, radius)
        cut, _ = gmsh.model.occ.cut([(2, rectangle)], [(2, disk)])
        gmsh.model.occ.synchronize()
        surfaces = [tag for dim, tag in cut if dim == 2]
        gmsh.model.addPhysicalGroup(2, surfaces, 1)
        gmsh.model.setPhysicalName(2, 1, "plate")
        boundary = gmsh.model.getBoundary(cut, oriented=False)
        groups = _classify_rectangle_with_circle(
            gmsh.model,
            boundary,
            length=length,
            y_min=y_min,
            y_max=y_max,
            circle_center=center,
            radius=radius,
        )
        for name, marker in (("left", 11), ("right", 12), ("walls", 13), ("circle", 14)):
            gmsh.model.addPhysicalGroup(1, groups[name], marker)
            gmsh.model.setPhysicalName(1, marker, name)
        gmsh.option.setNumber("Mesh.MeshSizeMin", mesh_size * 0.45)
        gmsh.option.setNumber("Mesh.MeshSizeMax", mesh_size)
        gmsh.model.mesh.generate(2)
    mesh_data = gmshio.model_to_mesh(gmsh.model, comm, rank=0, gdim=2)
    if comm.rank == 0:
        gmsh.finalize()
    return mesh_data


def channel_with_cylinder(
    comm: Any,
    *,
    length: float = 2.2,
    height: float = 0.41,
    center: tuple[float, float] = (0.2, 0.2),
    radius: float = 0.05,
    mesh_size: float = 0.06,
) -> Any:
    """Canal con obstáculo, grupos 1/21/22/23/24 (fluido/fronteras)."""

    import gmsh
    from dolfinx.io import gmsh as gmshio

    if comm.rank == 0:
        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("channel-with-cylinder")
        rectangle = gmsh.model.occ.addRectangle(0.0, 0.0, 0.0, length, height)
        disk = gmsh.model.occ.addDisk(center[0], center[1], 0.0, radius, radius)
        cut, _ = gmsh.model.occ.cut([(2, rectangle)], [(2, disk)])
        gmsh.model.occ.synchronize()
        surfaces = [tag for dim, tag in cut if dim == 2]
        gmsh.model.addPhysicalGroup(2, surfaces, 1)
        gmsh.model.setPhysicalName(2, 1, "fluid")
        boundary = gmsh.model.getBoundary(cut, oriented=False)
        groups = _classify_rectangle_with_circle(
            gmsh.model,
            boundary,
            length=length,
            y_min=0.0,
            y_max=height,
            circle_center=center,
            radius=radius,
        )
        for name, marker in (("left", 21), ("right", 22), ("walls", 23), ("circle", 24)):
            gmsh.model.addPhysicalGroup(1, groups[name], marker)
            gmsh.model.setPhysicalName(1, marker, name)
        gmsh.option.setNumber("Mesh.MeshSizeMin", mesh_size * 0.35)
        gmsh.option.setNumber("Mesh.MeshSizeMax", mesh_size)
        gmsh.model.mesh.generate(2)
    mesh_data = gmshio.model_to_mesh(gmsh.model, comm, rank=0, gdim=2)
    if comm.rank == 0:
        gmsh.finalize()
    return mesh_data
