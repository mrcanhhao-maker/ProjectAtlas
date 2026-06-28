from dataclasses import dataclass
from typing import Tuple


Point = Tuple[float, float]


@dataclass(frozen=True)
class PolygonRenderCommand:
    layer: str
    points: tuple[Point, ...]


@dataclass(frozen=True)
class RenderCommandQueue:
    commands: tuple[PolygonRenderCommand, ...]
