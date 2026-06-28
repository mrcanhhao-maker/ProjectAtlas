from atlas_platform.core_runtime import CoreRuntime
from renderer.render_extractor import RenderExtractor
from renderer.world_scene_adapter import WorldSceneAdapter
from world.boat_state import BoatState
from world.playable_world import CheckpointEntity, CurrentZoneEntity, PlayableWorld, RockEntity


def test_first_playable_river_runtime_emits_visible_world_render_commands():
    world = PlayableWorld(
        boat=BoatState(x=0.0, y=100.0, velocity_mps=0.0),
        rocks=(RockEntity(x=0.0, y=112.0, radius=1.2),),
        checkpoints=(CheckpointEntity(x=0.0, y=124.0, width=14.0, label="CP1"),),
        current_zones=(CurrentZoneEntity(x=0.0, y=118.0, width=10.0, height=6.0),),
    )
    runtime = CoreRuntime(
        world=world,
        scene_adapter=WorldSceneAdapter(),
        render_extractor=RenderExtractor(),
    )

    frame = runtime.update(0.0)
    commands = frame.render_queue.commands

    assert any(command.kind == "circle" for command in commands)
    assert any(command.kind == "line" for command in commands)
    assert any(command.kind == "rect" for command in commands)
    assert any(command.kind == "text" and command.text == "CP1" for command in commands)


def test_first_playable_river_objects_land_inside_720p_screen():
    from renderer.opencv_world_renderer import OpenCVWorldRenderer, RenderConfig
    from renderer.world_scene_adapter import BoatSnapshot

    renderer = OpenCVWorldRenderer(RenderConfig(width=1280, height=720, pixels_per_meter=18.0))
    boat = BoatSnapshot(x=0.0, y=100.0)

    rock = renderer.world_to_screen(0.0, 112.0, boat)
    current_zone = renderer.world_to_screen(0.0, 118.0, boat)
    checkpoint = renderer.world_to_screen(0.0, 124.0, boat)

    for sx, sy in (rock, current_zone, checkpoint):
        assert 0 <= sx < 1280
        assert 0 <= sy < 720

    assert rock[1] > current_zone[1] > checkpoint[1]
