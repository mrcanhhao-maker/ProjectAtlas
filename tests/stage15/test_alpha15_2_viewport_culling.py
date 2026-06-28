from world.camera import CameraState
from world.culling import ViewportCuller
from world.objects import WorldObject
from world.vector import Vec2
from world.viewport import ViewportFactory


def test_viewport_culler_only_returns_visible_world_objects():
    viewport = ViewportFactory(width=200, height=300).from_camera(
        CameraState(x=0, y=-100, boat_screen_y=0.78)
    )

    objects = (
        WorldObject("near", "rock", Vec2(0, -100), 20),
        WorldObject("edge", "checkpoint", Vec2(90, 40), 15),
        WorldObject("far", "tree", Vec2(0, -500), 20),
    )

    visible = ViewportCuller().visible_objects(objects, viewport)

    assert tuple(obj.object_id for obj in visible) == ("near", "edge")
    assert visible[0].screen_x == 100
    assert visible[0].screen_y == 150


def test_river_world_engine_builds_visible_objects_for_renderer():
    from world.engine import RiverWorldEngine
    from world.physics import StrokeInput
    from world.river_map import RiverMap

    engine = RiverWorldEngine(RiverMap.alpha15_1_level_1())
    snapshot = engine.step(StrokeInput(stroke_power=0.5, stroke_rate=20), dt=0.5)

    visible_ids = tuple(obj.object_id for obj in snapshot.frame.visible_objects)

    assert "waypoint:0" in visible_ids
    assert "checkpoint:start" in visible_ids
