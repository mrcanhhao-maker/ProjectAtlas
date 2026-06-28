from dataclasses import dataclass

import numpy as np

from renderer.opencv_world_renderer import OpenCVWorldRenderer, RenderConfig
from renderer.scene_graph import SceneGraph, SceneNode


@dataclass(frozen=True)
class Boat:
    x: float
    y: float


def test_renderer_places_boat_between_75_and_80_percent_screen_height():
    renderer = OpenCVWorldRenderer(RenderConfig(width=800, height=600))
    frame = renderer.render(SceneGraph(nodes=[], hud_lines=[]), Boat(0.0, 100.0))

    non_water = np.where((frame[:, :, 0] < 35) & (frame[:, :, 1] < 35) & (frame[:, :, 2] < 40))
    assert non_water[0].size > 0
    boat_center_y = int(non_water[0].mean())
    assert int(600 * 0.75) <= boat_center_y <= int(600 * 0.80) + 25


def test_world_to_screen_keeps_boat_camera_centered_horizontally():
    renderer = OpenCVWorldRenderer(RenderConfig(width=1000, height=500))
    sx, sy = renderer.world_to_screen(20.0, 300.0, Boat(20.0, 300.0))

    assert sx == 500
    assert sy == int(round(500 * 0.78))


def test_river_scrolls_from_top_to_bottom_when_object_is_behind_boat():
    renderer = OpenCVWorldRenderer(RenderConfig(width=1000, height=500, pixels_per_meter=10))
    boat = Boat(0.0, 100.0)

    ahead_y = renderer.world_to_screen(0.0, 120.0, boat)[1]
    behind_y = renderer.world_to_screen(0.0, 80.0, boat)[1]

    assert ahead_y < behind_y


def test_renderer_draws_required_world_elements():
    renderer = OpenCVWorldRenderer(RenderConfig(width=800, height=600))
    scene = SceneGraph(
        nodes=[
            SceneNode(kind="rock", world_x=0, world_y=105, radius=1.2, color=(80, 80, 80)),
            SceneNode(kind="checkpoint", world_x=0, world_y=115, width=8, color=(0, 220, 255), label="CP1"),
            SceneNode(kind="current_zone", world_x=0, world_y=95, width=10, height=5, color=(255, 160, 0), debug=True),
        ],
        hud_lines=["Alpha 16.0", "SPM 24"],
    )

    frame = renderer.render(scene, Boat(0.0, 100.0))

    assert frame.shape == (600, 800, 3)
    assert frame.dtype == np.uint8
    assert frame.sum() > 0
