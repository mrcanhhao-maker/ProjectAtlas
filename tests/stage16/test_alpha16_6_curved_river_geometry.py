from renderer.opencv_world_renderer import OpenCVWorldRenderer, RenderConfig
from renderer.render_queue import RenderQueue
from renderer.world_scene_adapter import BoatSnapshot


def test_renderer_supports_configurable_river_banks():
    config = RenderConfig(
        width=1000,
        height=600,
        pixels_per_meter=18.0,
        river_left_ratio=0.18,
        river_right_ratio=0.82,
    )
    renderer = OpenCVWorldRenderer(config)

    frame = renderer.render_queue(RenderQueue.from_commands(()), BoatSnapshot(x=0.0, y=0.0))

    assert tuple(frame[300, 50]) != tuple(frame[300, 500])
    assert tuple(frame[300, 950]) != tuple(frame[300, 500])
    assert tuple(frame[300, 500]) == (126, 92, 42)
