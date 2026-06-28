from dataclasses import dataclass

from renderer.world_scene_adapter import BoatSnapshot, WorldRenderSnapshot, WorldSceneAdapter


@dataclass(frozen=True)
class Rock:
    x: float
    y: float
    radius: float


@dataclass(frozen=True)
class Checkpoint:
    x: float
    y: float
    width: float
    label: str


@dataclass(frozen=True)
class CurrentZone:
    x: float
    y: float
    width: float
    height: float


def test_world_scene_adapter_converts_world_snapshot_to_scene_graph():
    snapshot = WorldRenderSnapshot(
        boat=BoatSnapshot(x=0.0, y=120.0),
        rocks=[Rock(x=2.0, y=128.0, radius=1.5)],
        checkpoints=[Checkpoint(x=0.0, y=150.0, width=12.0, label="CP1")],
        current_zones=[CurrentZone(x=-1.0, y=135.0, width=8.0, height=5.0)],
        hud_lines=["Alpha 16.1", "Boat y 120.0"],
    )

    scene = WorldSceneAdapter().build_scene(snapshot)

    assert len(scene.nodes) == 3
    assert scene.nodes[0].kind == "rock"
    assert scene.nodes[0].world_x == 2.0
    assert scene.nodes[1].kind == "checkpoint"
    assert scene.nodes[1].label == "CP1"
    assert scene.nodes[2].kind == "current_zone"
    assert scene.nodes[2].debug is True
    assert scene.hud_lines == ("Alpha 16.1", "Boat y 120.0")


def test_world_scene_adapter_output_renders_with_opencv_renderer():
    from renderer.opencv_world_renderer import OpenCVWorldRenderer, RenderConfig

    snapshot = WorldRenderSnapshot(
        boat=BoatSnapshot(x=0.0, y=100.0),
        rocks=[Rock(x=0.0, y=110.0, radius=1.0)],
        checkpoints=[Checkpoint(x=0.0, y=125.0, width=10.0, label="CP")],
        current_zones=[CurrentZone(x=0.0, y=95.0, width=10.0, height=5.0)],
        hud_lines=["Adapter Render"],
    )

    scene = WorldSceneAdapter().build_scene(snapshot)
    frame = OpenCVWorldRenderer(RenderConfig(width=640, height=360)).render(scene, snapshot.boat)

    assert frame.shape == (360, 640, 3)
    assert frame.sum() > 0

def test_world_scene_adapter_reads_world_object_position_for_first_playable_river():
    from world.objects import WorldObject
    from world.vector import Vec2

    snapshot = WorldRenderSnapshot(
        boat=BoatSnapshot(x=0.0, y=100.0),
        rocks=(WorldObject(object_id="rock:1", kind="rock", position=Vec2(2.0, 112.0), radius=1.4),),
        checkpoints=(WorldObject(object_id="checkpoint:1", kind="checkpoint", position=Vec2(0.0, 130.0), radius=6.0),),
        current_zones=(WorldObject(object_id="current:1", kind="current_zone", position=Vec2(-1.0, 118.0), radius=4.0),),
        hud_lines=("Alpha 16.5.1",),
    )

    scene = WorldSceneAdapter().build_scene(snapshot)

    assert len(scene.nodes) == 3
    assert scene.nodes[0].kind == "rock"
    assert scene.nodes[0].world_x == 2.0
    assert scene.nodes[0].world_y == 112.0
    assert scene.nodes[0].radius == 1.4

    assert scene.nodes[1].kind == "checkpoint"
    assert scene.nodes[1].world_x == 0.0
    assert scene.nodes[1].world_y == 130.0
    assert scene.nodes[1].width > 0

    assert scene.nodes[2].kind == "current_zone"
    assert scene.nodes[2].world_x == -1.0
    assert scene.nodes[2].world_y == 118.0
    assert scene.nodes[2].width > 0
