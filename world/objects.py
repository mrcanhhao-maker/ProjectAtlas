from dataclasses import dataclass

from world.vector import Vec2


@dataclass(frozen=True)
class WorldObject:
    object_id: str
    kind: str
    position: Vec2
    radius: float = 0.0

    def __post_init__(self) -> None:
        if not self.object_id:
            raise ValueError("object_id must not be empty")
        if not self.kind:
            raise ValueError("kind must not be empty")
        if self.radius < 0:
            raise ValueError("radius must not be negative")


@dataclass(frozen=True)
class VisibleObject:
    object_id: str
    kind: str
    screen_x: float
    screen_y: float
    radius: float
