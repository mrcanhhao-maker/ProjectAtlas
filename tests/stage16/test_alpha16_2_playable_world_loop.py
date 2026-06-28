from renderer.opencv_world_renderer import OpenCVWorldRenderer, RenderConfig
from renderer.world_scene_adapter import WorldSceneAdapter
from world.boat_state import BoatState
from world.playable_world import CheckpointEntity, CurrentZoneEntity, PlayableWorld, RockEntity


def test_boat_state_advances_forward_by_velocity_and_dt():
    boat = BoatState(x=0.0, y=10.0, velocity_mps=2.5)

    boat.advance(2.0)

    assert boat.y == 15.0


def test_boat_state_rejects_negative_dt():
    boat = BoatState()

    try:
        boat.advance(-0.1)
    except ValueError as exc:
        assert "dt" in str(exc)
    else:
        raise AssertionError("negative dt must fail")


def test_playable_world_update_moves_boat_and_snapshot_tracks_it():
    world = PlayableWorld(
        boat=BoatState(x=1.0, y=100.0, velocity_mps=3.0),
        rocks=(RockEntity(x=0.0, y=115.0, radius=1.0),),
        checkpoints=(CheckpointEntity(x=0.0, y=140.0, width=12.0, label="CP1"),),
        current_zones=(CurrentZoneEntity(x=0.0, y=125.0, width=8.0, height=5.0),),
    )

    world.update(1.5)
    snapshot = world.snapshot()

    assert snapshot.boat.x == 1.0
    assert snapshot.boat.y == 104.5
    assert len(snapshot.rocks) == 1
    assert len(snapshot.checkpoints) == 1
    assert len(snapshot.current_zones) == 1
    assert "Alpha 16.5" in snapshot.hud_lines[0]


def test_first_world_scene_render_loop_produces_frame_after_update():
    world = PlayableWorld(
        boat=BoatState(x=0.0, y=100.0, velocity_mps=4.0),
        rocks=(RockEntity(x=0.0, y=115.0, radius=1.0),),
        checkpoints=(CheckpointEntity(x=0.0, y=140.0, width=12.0, label="CP1"),),
        current_zones=(CurrentZoneEntity(x=0.0, y=125.0, width=8.0, height=5.0),),
    )

    world.update(1.0)
    snapshot = world.snapshot()
    scene = WorldSceneAdapter().build_scene(snapshot)
    frame = OpenCVWorldRenderer(RenderConfig(width=640, height=360)).render(scene, snapshot.boat)

    assert frame.shape == (360, 640, 3)
    assert frame.sum() > 0


def test_river_objects_scroll_down_when_boat_moves_forward():
    renderer = OpenCVWorldRenderer(RenderConfig(width=640, height=360, pixels_per_meter=10))
    world = PlayableWorld(boat=BoatState(x=0.0, y=100.0, velocity_mps=5.0))

    before_y = renderer.world_to_screen(0.0, 120.0, world.snapshot().boat)[1]
    world.update(1.0)
    after_y = renderer.world_to_screen(0.0, 120.0, world.snapshot().boat)[1]

    assert after_y > before_y
