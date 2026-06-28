from atlas_platform.core_runtime import CoreRuntime
from renderer.opencv_world_renderer import OpenCVWorldRenderer, RenderConfig
from renderer.render_extractor import RenderExtractor
from renderer.world_scene_adapter import WorldSceneAdapter
from world.boat_state import BoatState
from world.playable_world import CheckpointEntity, CurrentZoneEntity, PlayableWorld, RockEntity


def make_runtime() -> CoreRuntime:
    world = PlayableWorld(
        boat=BoatState(x=0.0, y=100.0, velocity_mps=3.0),
        rocks=(RockEntity(x=0.0, y=115.0, radius=1.0),),
        checkpoints=(CheckpointEntity(x=0.0, y=140.0, width=12.0, label="CP1"),),
        current_zones=(CurrentZoneEntity(x=0.0, y=125.0, width=8.0, height=5.0),),
    )
    return CoreRuntime(
        world=world,
        scene_adapter=WorldSceneAdapter(),
        render_extractor=RenderExtractor(),
    )


def test_core_runtime_updates_world_and_returns_platform_neutral_frame():
    runtime = make_runtime()

    frame = runtime.update(1.0)

    assert frame.boat_y == 103.0
    assert frame.boat_x == 0.0
    assert len(frame.render_queue.commands) > 0


def test_core_runtime_rejects_negative_dt():
    runtime = make_runtime()

    try:
        runtime.update(-0.01)
    except ValueError as exc:
        assert "dt" in str(exc)
    else:
        raise AssertionError("negative dt must fail")


def test_platform_neutral_frame_can_be_rendered_by_opencv_adapter():
    runtime = make_runtime()
    frame = runtime.update(1.0)

    image = OpenCVWorldRenderer(RenderConfig(width=640, height=360)).render_queue(
        frame.render_queue,
        type("Boat", (), {"x": frame.boat_x, "y": frame.boat_y})(),
    )

    assert image.shape == (360, 640, 3)
    assert image.sum() > 0


def test_core_runtime_does_not_depend_on_opencv_display():
    runtime = make_runtime()
    frame = runtime.update(0.5)

    assert hasattr(frame, "render_queue")
    assert hasattr(frame, "boat_x")
    assert hasattr(frame, "boat_y")
    assert frame.__class__.__name__ == "RuntimeFrame"
