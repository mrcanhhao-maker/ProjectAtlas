from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentForce:
    forward_acceleration: float = 0.0
    lateral_acceleration: float = 0.0

    def __post_init__(self) -> None:
        if not -20.0 <= self.forward_acceleration <= 20.0:
            raise ValueError("forward_acceleration is outside safe simulation range")
        if not -20.0 <= self.lateral_acceleration <= 20.0:
            raise ValueError("lateral_acceleration is outside safe simulation range")


@dataclass(frozen=True)
class PhysicsForces:
    rowing_acceleration: float
    environment: EnvironmentForce

    @property
    def total_forward_acceleration(self) -> float:
        return self.rowing_acceleration + self.environment.forward_acceleration

    @property
    def total_lateral_acceleration(self) -> float:
        return self.environment.lateral_acceleration
