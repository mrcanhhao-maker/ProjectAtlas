from renderer.opencv_world_renderer import OpenCVWorldRenderer, RenderConfig
from renderer.render_command import RenderCommand
from renderer.render_extractor import RenderExtractor
from renderer.render_queue import RenderQueue
from renderer.scene_graph import SceneGraph, SceneNode
from renderer.world_scene_adapter import BoatSnapshot


def test_render_queue_sorts_commands_by_layer():
    queue = RenderQueue.from_commands(
        [
            RenderCommand(layer=30, kind="circle", color=(1, 1, 1), radius=1),
            RenderCommand(layer=10, kind="rect", color=(2, 2, 2), width=1, height=1),
        ]
    )

    assert [command.layer for command in queue.commands] == [10, 30]


def test_render_command_rejects_invalid_kind_and_alpha():
    try:
        RenderCommand(layer=0, kind="sprite", color=(1, 1, 1))
    except ValueError as exc:
        assert "Unsupported" in str(exc)
    else:
        raise AssertionError("invalid command kind must fail")

    try:
        RenderCommand(layer=0, kind="circle", color=(1, 1, 1), alpha=2.0)
    except ValueError as exc:
        assert "alpha" in str(exc)
    else:
        raise AssertionError("invalid alpha must fail")


def test_render_extractor_converts_scene_graph_to_render_queue():
    scene = SceneGraph(
        nodes=(
            SceneNode(kind="current_zone", world_x=0, world_y=95, width=8, height=4, color=(255, 160, 0)),
            SceneNode(kind="checkpoint", world_x=0, world_y=120, width=10, label="CP1", color=(0, 220, 255)),
            SceneNode(kind="rock", world_x=2, world_y=110, radius=1.2, color=(80, 80, 80)),
        ),
        hud_lines=("Alpha 16.3",),
    )

    queue = RenderExtractor().extract(scene)

    assert [command.kind for command in queue.commands] == ["rect", "line", "text", "circle", "text"]
    assert queue.commands[-1].text == "Alpha 16.3"


def test_opencv_renderer_can_render_from_render_queue():
    scene = SceneGraph(
        nodes=(
            SceneNode(kind="current_zone", world_x=0, world_y=95, width=8, height=4, color=(255, 160, 0)),
            SceneNode(kind="checkpoint", world_x=0, world_y=120, width=10, label="CP1", color=(0, 220, 255)),
            SceneNode(kind="rock", world_x=2, world_y=110, radius=1.2, color=(80, 80, 80)),
        ),
        hud_lines=("Alpha 16.3",),
    )
    queue = RenderExtractor().extract(scene)

    frame = OpenCVWorldRenderer(RenderConfig(width=640, height=360)).render_queue(queue, BoatSnapshot(x=0, y=100))

    assert frame.shape == (360, 640, 3)
    assert frame.sum() > 0
