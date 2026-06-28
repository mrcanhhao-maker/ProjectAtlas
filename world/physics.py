from dataclasses import dataclass

from world.forces import EnvironmentForce, PhysicsForces


@dataclass(frozen=True)
class StrokeInput:
    stroke_power: float
    stroke_rate: float


@dataclass(frozen=True)
class BoatState:
    lane_x: float
    distance: float
    speed: float


class RowingPhysics:
    def __init__(self, drag: float = 0.92, max_speed: float = 18.0) -> None:
        if not 0 < drag <= 1:
            raise ValueError("drag must be between 0 and 1")
        if max_speed <= 0:
            raise ValueError("max_speed must be positive")
        self.drag = drag
        self.max_speed = max_speed

    def step(
        self,
        state: BoatState,
        stroke: StrokeInput,
        dt: float,
        environment: EnvironmentForce | None = None,
    ) -> BoatState:
        if dt <= 0:
            raise ValueError("dt must be positive")

        power = max(0.0, min(1.0, stroke.stroke_power))
        rate_bonus = max(0.0, min(1.0, stroke.stroke_rate / 36.0))
        rowing_acceleration = power * (6.0 + 4.0 * rate_bonus)
        forces = PhysicsForces(
            rowing_acceleration=rowing_acceleration,
            environment=environment or EnvironmentForce(),
        )

        speed = min(
            self.max_speed,
            max(0.0, (state.speed * self.drag) + forces.total_forward_acceleration * dt),
        )
        distance = state.distance + speed * dt
        lane_x = state.lane_x + forces.total_lateral_acceleration * dt

        return BoatState(
            lane_x=lane_x,
            distance=distance,
            speed=speed,
        )
