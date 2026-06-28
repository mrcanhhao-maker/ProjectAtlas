from world.procedural import ProceduralRiverGenerator
from world.streaming import RiverChunkGenerator


def test_procedural_river_generator_is_stable_for_same_seed():
    first = ProceduralRiverGenerator("atlas-daily-river").chunk_spec(42)
    second = ProceduralRiverGenerator("atlas-daily-river").chunk_spec(42)

    assert first == second


def test_procedural_river_generator_changes_with_different_seed():
    first = ProceduralRiverGenerator("atlas-daily-river").chunk_spec(42)
    second = ProceduralRiverGenerator("atlas-weekly-river").chunk_spec(42)

    assert first != second


def test_river_chunk_generator_uses_procedural_seed():
    generator_a = RiverChunkGenerator(
        chunk_height=600,
        procedural=ProceduralRiverGenerator("seed-a"),
    )
    generator_b = RiverChunkGenerator(
        chunk_height=600,
        procedural=ProceduralRiverGenerator("seed-a"),
    )
    generator_c = RiverChunkGenerator(
        chunk_height=600,
        procedural=ProceduralRiverGenerator("seed-c"),
    )

    chunk_a = generator_a.chunk_for_index(7)
    chunk_b = generator_b.chunk_for_index(7)
    chunk_c = generator_c.chunk_for_index(7)

    assert chunk_a.objects == chunk_b.objects
    assert chunk_a.objects != chunk_c.objects
