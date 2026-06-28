from dataclasses import dataclass
from typing import Tuple

from world.vector import Vec2


@dataclass(frozen=True)
class RiverWaypoint:
    position: Vec2
    width: float


@dataclass(frozen=True)
class RiverObstacle:
    position: Vec2
    radius: float
    kind: str


@dataclass(frozen=True)
class RiverCheckpoint:
    position: Vec2
    name: str


@dataclass(frozen=True)
class RiverMap:
    name: str
    waypoints: Tuple[RiverWaypoint, ...]
    obstacles: Tuple[RiverObstacle, ...]
    checkpoints: Tuple[RiverCheckpoint, ...]

    @staticmethod
    def alpha15_1_level_1() -> "RiverMap":
        return RiverMap(
            name="River Level 1 - Calm Water",
            waypoints=(
                RiverWaypoint(Vec2(0, 0), 420),
                RiverWaypoint(Vec2(20, -600), 400),
                RiverWaypoint(Vec2(-35, -1200), 380),
                RiverWaypoint(Vec2(15, -1800), 360),
            ),
            obstacles=(),
            checkpoints=(
                RiverCheckpoint(Vec2(0, 0), "start"),
                RiverCheckpoint(Vec2(15, -1800), "finish"),
            ),
        )
