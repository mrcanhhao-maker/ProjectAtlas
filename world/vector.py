from dataclasses import dataclass


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def add(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def scale(self, value: float) -> "Vec2":
        return Vec2(self.x * value, self.y * value)
