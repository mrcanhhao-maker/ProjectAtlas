from dataclasses import dataclass

from world.camera import CameraState
from world.vector import Vec2


@dataclass(frozen=True)
class Viewport:
    center: Vec2
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("viewport width must be positive")
        if self.height <= 0:
            raise ValueError("viewport height must be positive")

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

    def contains_circle(self, position: Vec2, radius: float = 0.0) -> bool:
        if radius < 0:
            raise ValueError("radius must not be negative")

        return (
            position.x + radius >= self.left
            and position.x - radius <= self.right
            and position.y + radius >= self.top
            and position.y - radius <= self.bottom
        )


class ViewportFactory:
    def __init__(self, width: float = 720.0, height: float = 1280.0) -> None:
        if width <= 0:
            raise ValueError("viewport width must be positive")
        if height <= 0:
            raise ValueError("viewport height must be positive")
        self.width = width
        self.height = height

    def from_camera(self, camera: CameraState) -> Viewport:
        return Viewport(
            center=Vec2(camera.x, camera.y),
            width=self.width,
            height=self.height,
        )
