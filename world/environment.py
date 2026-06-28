from world.forces import EnvironmentForce
from world.procedural import ProceduralRiverGenerator


class RiverEnvironment:
    def __init__(self, procedural: ProceduralRiverGenerator, chunk_height: float = 600.0) -> None:
        if chunk_height <= 0:
            raise ValueError("chunk_height must be positive")
        self.procedural = procedural
        self.chunk_height = chunk_height

    def force_at_distance(self, distance: float) -> EnvironmentForce:
        if distance < 0:
            raise ValueError("distance must not be negative")

        chunk_index = int(distance // self.chunk_height)
        spec = self.procedural.chunk_spec(chunk_index)

        return EnvironmentForce(
            forward_acceleration=spec.flow_speed,
            lateral_acceleration=spec.lateral_flow,
        )
