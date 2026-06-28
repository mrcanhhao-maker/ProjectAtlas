from typing import Tuple

from world.current import CurrentZone
from world.forces import EnvironmentForce
from world.procedural import ProceduralRiverGenerator
from world.vector import Vec2


class RiverEnvironment:
    def __init__(self, procedural: ProceduralRiverGenerator, chunk_height: float = 600.0) -> None:
        if chunk_height <= 0:
            raise ValueError("chunk_height must be positive")
        self.procedural = procedural
        self.chunk_height = chunk_height

    def force_at_distance(self, distance: float) -> EnvironmentForce:
        return self.force_at_position(lane_x=0.0, distance=distance)

    def force_at_position(self, lane_x: float, distance: float) -> EnvironmentForce:
        if distance < 0:
            raise ValueError("distance must not be negative")

        position = Vec2(lane_x, -distance)
        for zone in self.current_zones_near_distance(distance):
            if zone.contains(position):
                return zone.force

        chunk_index = int(distance // self.chunk_height)
        spec = self.procedural.chunk_spec(chunk_index)
        return EnvironmentForce(
            forward_acceleration=spec.flow_speed,
            lateral_acceleration=spec.lateral_flow,
        )

    def current_zones_near_distance(self, distance: float) -> Tuple[CurrentZone, ...]:
        if distance < 0:
            raise ValueError("distance must not be negative")

        chunk_index = int(distance // self.chunk_height)
        zones = []
        for index in range(max(0, chunk_index - 1), chunk_index + 2):
            zones.extend(self.current_zones_for_chunk(index))
        return tuple(zones)

    def current_zones_for_chunk(self, chunk_index: int) -> Tuple[CurrentZone, ...]:
        if chunk_index < 0:
            raise ValueError("chunk_index must not be negative")

        spec = self.procedural.chunk_spec(chunk_index)
        start_y = -((chunk_index + 1) * self.chunk_height)
        center_y = start_y + self.chunk_height / 2

        return (
            CurrentZone(
                zone_id=f"chunk:{chunk_index}:current:center",
                center=Vec2(spec.center_x, center_y),
                width=spec.width * 0.45,
                height=self.chunk_height,
                force=EnvironmentForce(
                    forward_acceleration=spec.flow_speed + 0.35,
                    lateral_acceleration=spec.lateral_flow,
                ),
                drag_multiplier=0.92,
            ),
            CurrentZone(
                zone_id=f"chunk:{chunk_index}:current:left_bank",
                center=Vec2(spec.center_x - spec.width * 0.38, center_y),
                width=spec.width * 0.25,
                height=self.chunk_height,
                force=EnvironmentForce(
                    forward_acceleration=max(0.0, spec.flow_speed - 0.35),
                    lateral_acceleration=spec.lateral_flow + 0.12,
                ),
                drag_multiplier=1.12,
            ),
            CurrentZone(
                zone_id=f"chunk:{chunk_index}:current:right_bank",
                center=Vec2(spec.center_x + spec.width * 0.38, center_y),
                width=spec.width * 0.25,
                height=self.chunk_height,
                force=EnvironmentForce(
                    forward_acceleration=max(0.0, spec.flow_speed - 0.35),
                    lateral_acceleration=spec.lateral_flow - 0.12,
                ),
                drag_multiplier=1.12,
            ),
        )
