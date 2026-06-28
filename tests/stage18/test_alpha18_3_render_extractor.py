from render_extractor import RenderExtractor
from river_geometry import RiverCrossSection, RiverGeometryEngine, RiverPath
from scene_graph import RiverSceneNodeFactory, SceneGraph


def test_render_extractor_converts_river_scene_node_to_polygon_command():
    path = RiverPath([
        (320.0, 0.0),
        (330.0, 100.0),
    ])
    section = RiverCrossSection(center_x=320.0, width=120.0)
    geometry = RiverGeometryEngine().build(path, section)

    scene = SceneGraph.empty().add(
        RiverSceneNodeFactory().create(geometry)
    )

    queue = RenderExtractor().extract(scene)

    assert len(queue.commands) == 1
    assert queue.commands[0].layer == "river"
    assert queue.commands[0].points == geometry.polygon.points


def test_render_extractor_ignores_unknown_node_types():
    scene = SceneGraph.empty()

    queue = RenderExtractor().extract(scene)

    assert queue.commands == ()
