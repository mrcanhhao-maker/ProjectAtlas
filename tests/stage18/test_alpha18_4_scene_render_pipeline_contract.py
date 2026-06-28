from render_extractor import RenderExtractor
from river_geometry import RiverCrossSection, RiverGeometryEngine, RiverPath
from scene_graph import RiverSceneNodeFactory, SceneGraph


def test_scene_render_pipeline_contract():
    path = RiverPath([
        (320.0, 0.0),
        (325.0, 100.0),
        (330.0, 200.0),
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
