from dataclasses import dataclass
from typing import Tuple

from .banks import RiverBanks


Point = Tuple[float, float]


@dataclass(frozen=True)
class RiverPolygon:
    points: tuple[Point, ...]

    def __post_init__(self) -> None:
        if len(self.points) < 4:
            raise ValueError("river polygon requires at least four points")


class RiverPolygonBuilder:
    """
    Builds a closed render-ready polygon from generated river banks.

    Renderer receives this polygon and only draws it.
    Renderer must not calculate banks or river shape.
    """

    def build(self, banks: RiverBanks) -> RiverPolygon:
        if len(banks.left_bank) != len(banks.right_bank):
            raise ValueError("left and right river banks must have the same sample count")
        if len(banks.left_bank) < 2:
            raise ValueError("river polygon requires at least two samples per bank")

        points = tuple(banks.left_bank) + tuple(reversed(banks.right_bank))
        return RiverPolygon(points=points)
