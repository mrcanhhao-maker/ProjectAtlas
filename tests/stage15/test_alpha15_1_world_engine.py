from world.engine import RiverWorldEngine
from world.physics import StrokeInput
from world.river_map import RiverMap


def test_river_world_engine_moves_world_top_down_from_strokes():
    engine = RiverWorldEngine(RiverMap.alpha15_1_level_1())

    first = engine.step(StrokeInput(stroke_power=0.8, stroke_rate=24), dt=0.5)
    second = engine.step(StrokeInput(stroke_power=0.8, stroke_rate=24), dt=0.5)

    assert second.boat.distance > first.boat.distance
    assert second.boat.speed > 0
    assert second.frame.camera_y < first.frame.camera_y
    assert second.frame.hud.checkpoint == "start"
    assert second.frame.hud.finished is False


def test_river_world_engine_reaches_finish_checkpoint():
    engine = RiverWorldEngine(RiverMap.alpha15_1_level_1())

    snapshot = None
    for _ in range(260):
        snapshot = engine.step(StrokeInput(stroke_power=1.0, stroke_rate=32), dt=0.5)

    assert snapshot is not None
    assert snapshot.frame.hud.checkpoint == "finish"
    assert snapshot.frame.hud.finished is True
