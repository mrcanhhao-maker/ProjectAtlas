from dataclasses import dataclass
from typing import Iterable, Tuple


Point = Tuple[float, float]


@dataclass(frozen=True)
class RiverPath:
    """
    Ordered center line of the river.

    The renderer must never infer geometry directly.
    All river geometry will be derived from this path.
    """

    points: tuple[Point, ...]

    def __init__(self, points: Iterable[Point]):
        pts = tuple(points)
        if len(pts) < 2:
            raise ValueError("river path requires at least two points")
        object.__setattr__(self, "points", pts)

    @property
    def segments(self) -> int:
        return len(self.points) - 1

    @property
    def start(self) -> Point:
        return self.points[0]

    @property
    def end(self) -> Point:
        return self.points[-1]
