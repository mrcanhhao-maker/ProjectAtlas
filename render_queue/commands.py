from dataclasses import dataclass
from typing import Tuple

from river_geometry import RiverPolygon


Point = Tuple[float, float]


@dataclass(frozen=True)
class PolygonRenderCommand:
    layer: str
    points: tuple[Point, ...]


@dataclass(frozen=True)
class RenderCommandQueue:
    commands: tuple[PolygonRenderCommand, ...]

    @classmethod
    def from_river_polygon(cls, polygon: RiverPolygon) -> "RenderCommandQueue":
        return cls(commands=(
            PolygonRenderCommand(
                layer="river",
                points=polygon.points,
            ),
        ))
