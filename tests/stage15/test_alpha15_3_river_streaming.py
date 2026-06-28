from world.engine import RiverWorldEngine
from world.physics import StrokeInput
from world.river_map import RiverMap
from world.streaming import RiverChunkGenerator, RiverStream
from world.vector import Vec2
from world.viewport import Viewport


def test_river_stream_loads_nearby_chunks_and_unloads_old_chunks():
    stream = RiverStream(
        generator=RiverChunkGenerator(chunk_height=100),
        preload_before=1,
        preload_after=2,
    )

    first_objects = stream.update(Viewport(center=Vec2(0, -50), width=200, height=300))
    assert tuple(stream.loaded_chunks) == (0, 1, 2)
    assert any(obj.object_id == "chunk:0:river_center" for obj in first_objects)

    second_objects = stream.update(Viewport(center=Vec2(0, -350), width=200, height=300))
    assert tuple(stream.loaded_chunks) == (2, 3, 4, 5)
    assert all(not obj.object_id.startswith("chunk:0:") for obj in second_objects)


def test_world_engine_renderer_receives_streamed_river_objects():
    engine = RiverWorldEngine(RiverMap.alpha15_1_level_1())

    snapshot = engine.step(StrokeInput(stroke_power=1.0, stroke_rate=30), dt=0.5)
    visible_ids = tuple(obj.object_id for obj in snapshot.frame.visible_objects)

    assert any(object_id.startswith("chunk:") for object_id in visible_ids)
    assert any(object_id.endswith(":river_center") for object_id in visible_ids)
