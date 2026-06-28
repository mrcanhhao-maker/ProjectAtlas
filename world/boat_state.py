from dataclasses import dataclass


@dataclass
class BoatState:
    x: float = 0.0
    y: float = 0.0
    velocity_mps: float = 0.0

    def advance(self, dt: float) -> None:
        if dt < 0:
            raise ValueError("dt must be non-negative")
        self.y += self.velocity_mps * dt
