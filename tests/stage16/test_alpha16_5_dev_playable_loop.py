from atlas_platform.dev_playable_loop import DevPlayableLoop


class FakeRuntime:
    def __init__(self):
        self.calls = 0

    def update(self, dt):
        self.calls += 1
        assert dt >= 0
        return {"frame": self.calls}


class FakeDisplay:
    def __init__(self):
        self.frames = []

    def present(self, frame):
        self.frames.append(frame)


def test_dev_playable_loop_rejects_invalid_target_fps():
    try:
        DevPlayableLoop(runtime=FakeRuntime(), display=FakeDisplay(), target_fps=0)
    except ValueError as exc:
        assert "target_fps" in str(exc)
    else:
        raise AssertionError("invalid target_fps must fail")


def test_alpha16_5_runner_builds_world_with_playable_content():
    from apps.dev_runner.alpha16_5_playable_river import build_world

    world = build_world()

    assert world.boat.velocity_mps > 0
    assert len(world.rocks) >= 5
    assert len(world.checkpoints) >= 3
    assert len(world.current_zones) >= 3


def test_alpha16_5_runtime_can_produce_renderable_frame():
    from apps.dev_runner.alpha16_5_playable_river import build_world
    from atlas_platform.core_runtime import CoreRuntime
    from renderer.opencv_world_renderer import OpenCVWorldRenderer, RenderConfig
    from renderer.render_extractor import RenderExtractor
    from renderer.world_scene_adapter import BoatSnapshot, WorldSceneAdapter

    runtime = CoreRuntime(
        world=build_world(),
        scene_adapter=WorldSceneAdapter(),
        render_extractor=RenderExtractor(),
    )

    frame = runtime.update(1 / 60)
    image = OpenCVWorldRenderer(RenderConfig(width=640, height=360)).render_queue(
        frame.render_queue,
        BoatSnapshot(x=frame.boat_x, y=frame.boat_y),
    )

    assert image.shape == (360, 640, 3)
    assert image.sum() > 0
