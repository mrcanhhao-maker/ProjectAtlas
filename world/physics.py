from dataclasses import dataclass


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

    def step(self, state: BoatState, stroke: StrokeInput, dt: float) -> BoatState:
        if dt <= 0:
            raise ValueError("dt must be positive")

        power = max(0.0, min(1.0, stroke.stroke_power))
        rate_bonus = max(0.0, min(1.0, stroke.stroke_rate / 36.0))
        acceleration = power * (6.0 + 4.0 * rate_bonus)

        speed = min(self.max_speed, (state.speed * self.drag) + acceleration * dt)
        distance = state.distance + speed * dt

        return BoatState(
            lane_x=state.lane_x,
            distance=distance,
            speed=speed,
        )
