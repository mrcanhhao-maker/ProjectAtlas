from dataclasses import dataclass

from world.forces import EnvironmentForce
from world.vector import Vec2


@dataclass(frozen=True)
class CurrentZone:
    zone_id: str
    center: Vec2
    width: float
    height: float
    force: EnvironmentForce
    drag_multiplier: float = 1.0

    def __post_init__(self) -> None:
        if not self.zone_id:
            raise ValueError("zone_id must not be empty")
        if self.width <= 0:
            raise ValueError("current zone width must be positive")
        if self.height <= 0:
            raise ValueError("current zone height must be positive")
        if self.drag_multiplier <= 0:
            raise ValueError("drag_multiplier must be positive")

    @property
    def left(self) -> float:
        return self.center.x - self.width / 2

    @property
    def right(self) -> float:
        return self.center.x + self.width / 2

    @property
    def top(self) -> float:
        return self.center.y - self.height / 2

    @property
    def bottom(self) -> float:
        return self.center.y + self.height / 2

    def contains(self, position: Vec2) -> bool:
        return (
            self.left <= position.x <= self.right
            and self.top <= position.y <= self.bottom
        )
