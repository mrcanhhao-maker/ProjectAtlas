from world.collision import CollisionEngine
from world.objects import WorldObject
from world.physics import BoatState
from world.procedural import ProceduralRiverGenerator
from world.streaming import RiverChunkGenerator
from world.vector import Vec2


def test_collision_engine_detects_boat_rock_overlap():
    boat = BoatState(lane_x=0.0, distance=100.0, speed=4.0)
    rock = WorldObject("rock-1", "rock", Vec2(0.0, -100.0), 34.0)

    report = CollisionEngine(boat_radius=28.0).detect(boat, (rock,))

    assert report.has_collision is True
    assert report.collisions[0].object_id == "rock-1"
    assert report.collisions[0].kind == "rock"


def test_collision_engine_ignores_non_collision_objects():
    boat = BoatState(lane_x=0.0, distance=100.0, speed=4.0)
    river_center = WorldObject("river", "river_center", Vec2(0.0, -100.0), 200.0)

    report = CollisionEngine().detect(boat, (river_center,))

    assert report.has_collision is False
    assert report.collisions == ()


def test_procedural_chunk_can_generate_rocks_after_safe_intro():
    generator = RiverChunkGenerator(
        chunk_height=600.0,
        procedural=ProceduralRiverGenerator("atlas-rock-test"),
    )

    intro_chunk = generator.chunk_for_index(0)
    later_chunks = [generator.chunk_for_index(index) for index in range(2, 12)]

    assert all(obj.kind != "rock" for obj in intro_chunk.objects)
    assert any(obj.kind == "rock" for chunk in later_chunks for obj in chunk.objects)
