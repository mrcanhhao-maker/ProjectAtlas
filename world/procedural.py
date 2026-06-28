from dataclasses import dataclass
import hashlib
import random


@dataclass(frozen=True)
class ProceduralRiverChunkSpec:
    center_x: float
    width: float
    flow_speed: float
    lateral_flow: float
    rock_offset_x: float | None
    rock_offset_y: float | None


class ProceduralRiverGenerator:
    def __init__(self, seed: str) -> None:
        if not seed:
            raise ValueError("seed must not be empty")
        self.seed = seed

    def chunk_spec(self, chunk_index: int) -> ProceduralRiverChunkSpec:
        if chunk_index < 0:
            raise ValueError("chunk_index must not be negative")

        rng = random.Random(self._stable_int(chunk_index))

        center_x = rng.uniform(-90.0, 90.0)
        width = rng.uniform(280.0, 460.0)
        flow_speed = rng.uniform(0.6, 1.4)
        lateral_flow = rng.uniform(-0.25, 0.25)
        has_rock = chunk_index >= 2 and rng.random() >= 0.35
        rock_offset_x = rng.uniform(-width * 0.32, width * 0.32) if has_rock else None
        rock_offset_y = rng.uniform(120.0, 480.0) if has_rock else None

        return ProceduralRiverChunkSpec(
            center_x=round(center_x, 3),
            width=round(width, 3),
            flow_speed=round(flow_speed, 3),
            lateral_flow=round(lateral_flow, 3),
            rock_offset_x=round(rock_offset_x, 3) if rock_offset_x is not None else None,
            rock_offset_y=round(rock_offset_y, 3) if rock_offset_y is not None else None,
        )

    def _stable_int(self, chunk_index: int) -> int:
        key = f"{self.seed}:{chunk_index}".encode("utf-8")
        digest = hashlib.sha256(key).hexdigest()
        return int(digest[:16], 16)
