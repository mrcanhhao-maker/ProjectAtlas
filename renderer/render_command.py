from dataclasses import dataclass
from typing import Tuple


Color = Tuple[int, int, int]
Point = Tuple[float, float]


@dataclass(frozen=True)
class RenderCommand:
    layer: int
    kind: str
    color: Color
    world_x: float = 0.0
    world_y: float = 0.0
    radius: float = 0.0
    width: float = 0.0
    height: float = 0.0
    points: Tuple[Point, ...] = ()
    text: str = ""
    font_scale: float = 0.7
    thickness: int = 2
    alpha: float = 1.0

    def __post_init__(self):
        if not 0.0 <= self.alpha <= 1.0:
            raise ValueError("alpha must be between 0.0 and 1.0")
        if self.kind not in {"circle", "line", "rect", "polygon", "text"}:
            raise ValueError(f"Unsupported render command kind: {self.kind}")
