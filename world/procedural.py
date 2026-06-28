from dataclasses import dataclass
import hashlib
import random


@dataclass(frozen=True)
class ProceduralRiverChunkSpec:
    center_x: float
    width: float
    flow_speed: float


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

        return ProceduralRiverChunkSpec(
            center_x=round(center_x, 3),
            width=round(width, 3),
            flow_speed=round(flow_speed, 3),
        )

    def _stable_int(self, chunk_index: int) -> int:
        key = f"{self.seed}:{chunk_index}".encode("utf-8")
        digest = hashlib.sha256(key).hexdigest()
        return int(digest[:16], 16)
