from dataclasses import dataclass
from typing import Tuple

from world.objects import WorldObject
from world.procedural import ProceduralRiverGenerator
from world.vector import Vec2
from world.viewport import Viewport


@dataclass(frozen=True)
class RiverChunk:
    index: int
    start_y: float
    end_y: float
    objects: Tuple[WorldObject, ...]

    def __post_init__(self) -> None:
        if self.end_y <= self.start_y:
            raise ValueError("chunk end_y must be greater than start_y")


class RiverChunkGenerator:
    def __init__(
        self,
        chunk_height: float = 600.0,
        procedural: ProceduralRiverGenerator | None = None,
    ) -> None:
        if chunk_height <= 0:
            raise ValueError("chunk_height must be positive")
        self.chunk_height = chunk_height
        self.procedural = procedural or ProceduralRiverGenerator(seed="atlas-alpha15")

    def chunk_for_index(self, index: int) -> RiverChunk:
        start_y = -((index + 1) * self.chunk_height)
        end_y = -(index * self.chunk_height)
        spec = self.procedural.chunk_spec(index)
        bend_x = spec.center_x
        river_width = spec.width

        objects = [
            WorldObject(
                object_id=f"chunk:{index}:river_center",
                kind="river_center",
                position=Vec2(bend_x, start_y + self.chunk_height / 2),
                radius=river_width / 2,
            )
        ]

        if spec.rock_offset_x is not None and spec.rock_offset_y is not None:
            objects.append(
                WorldObject(
                    object_id=f"chunk:{index}:rock:0",
                    kind="rock",
                    position=Vec2(bend_x + spec.rock_offset_x, start_y + spec.rock_offset_y),
                    radius=34.0,
                )
            )

        return RiverChunk(
            index=index,
            start_y=start_y,
            end_y=end_y,
            objects=tuple(objects),
        )

class RiverStream:
    def __init__(
        self,
        generator: RiverChunkGenerator | None = None,
        preload_before: int = 1,
        preload_after: int = 3,
    ) -> None:
        if preload_before < 0:
            raise ValueError("preload_before must not be negative")
        if preload_after < 0:
            raise ValueError("preload_after must not be negative")

        self.generator = generator or RiverChunkGenerator()
        self.preload_before = preload_before
        self.preload_after = preload_after
        self.loaded_chunks: dict[int, RiverChunk] = {}

    def update(self, viewport: Viewport) -> Tuple[WorldObject, ...]:
        current_index = self._index_for_y(viewport.center.y)
        wanted = set(
            range(
                max(0, current_index - self.preload_before),
                current_index + self.preload_after + 1,
            )
        )

        for index in wanted:
            if index not in self.loaded_chunks:
                self.loaded_chunks[index] = self.generator.chunk_for_index(index)

        for index in tuple(self.loaded_chunks):
            if index not in wanted:
                del self.loaded_chunks[index]

        objects = []
        for index in sorted(self.loaded_chunks):
            objects.extend(self.loaded_chunks[index].objects)

        return tuple(objects)

    def _index_for_y(self, y: float) -> int:
        if y >= 0:
            return 0
        return int(abs(y) // self.generator.chunk_height)
