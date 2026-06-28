from render_queue import RenderCommandQueue
from river_geometry import (
    RiverCrossSection,
    RiverGeometryEngine,
    RiverPath,
)


def test_complete_river_geometry_pipeline_contract():
    path = RiverPath(
        [
            (320.0, 0.0),
            (325.0, 120.0),
            (330.0, 240.0),
            (335.0, 360.0),
        ]
    )

    section = RiverCrossSection(
        center_x=320.0,
        width=140.0,
    )

    geometry = RiverGeometryEngine().build(path, section)

    queue = RenderCommandQueue.from_river_polygon(
        geometry.polygon
    )

    assert len(queue.commands) == 1

    command = queue.commands[0]

    assert command.layer == "river"

    assert command.points == geometry.polygon.points

    assert len(geometry.banks.left_bank) == len(path.points)
    assert len(geometry.banks.right_bank) == len(path.points)

    assert len(geometry.mesh.vertices) == len(path.points) * 2
    assert len(geometry.mesh.triangles) == (len(path.points) - 1) * 2
