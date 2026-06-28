import pytest

from scene_graph import SceneGraph, SceneNode


def test_scene_graph_starts_empty():
    scene = SceneGraph.empty()

    assert scene.nodes == ()


def test_scene_graph_adds_node_immutably():
    scene = SceneGraph.empty()
    node = SceneNode(
        node_type="river",
        payload={"polygon_points": ((0.0, 0.0), (1.0, 1.0))},
    )

    next_scene = scene.add(node)

    assert scene.nodes == ()
    assert next_scene.nodes == (node,)


def test_scene_node_rejects_empty_type():
    with pytest.raises(ValueError):
        SceneNode(node_type="", payload={})
