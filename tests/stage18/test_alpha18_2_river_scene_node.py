from river_geometry import RiverCrossSection, RiverGeometryEngine, RiverPath
from scene_graph import RiverSceneNodeFactory, SceneGraph


def test_river_scene_node_factory_exports_geometry_payload():
    path = RiverPath([
        (320.0, 0.0),
        (330.0, 100.0),
    ])
    section = RiverCrossSection(center_x=320.0, width=120.0)
    geometry = RiverGeometryEngine().build(path, section)

    node = RiverSceneNodeFactory().create(geometry)

    assert node.node_type == "river"
    assert node.payload["polygon_points"] == geometry.polygon.points
    assert node.payload["mesh_vertices"] == geometry.mesh.vertices
    assert node.payload["mesh_triangles"] == geometry.mesh.triangles


def test_river_scene_node_can_be_added_to_scene_graph():
    path = RiverPath([
        (320.0, 0.0),
        (330.0, 100.0),
    ])
    section = RiverCrossSection(center_x=320.0, width=120.0)
    geometry = RiverGeometryEngine().build(path, section)

    node = RiverSceneNodeFactory().create(geometry)
    scene = SceneGraph.empty().add(node)

    assert scene.nodes == (node,)
