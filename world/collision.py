from dataclasses import dataclass
import math
from typing import Iterable, Tuple

from world.objects import WorldObject
from world.physics import BoatState


@dataclass(frozen=True)
class CollisionResult:
    object_id: str
    kind: str
    distance: float


@dataclass(frozen=True)
class CollisionReport:
    collisions: Tuple[CollisionResult, ...]

    @property
    def has_collision(self) -> bool:
        return bool(self.collisions)


class CollisionEngine:
    def __init__(self, boat_radius: float = 28.0) -> None:
        if boat_radius <= 0:
            raise ValueError("boat_radius must be positive")
        self.boat_radius = boat_radius

    def detect(
        self,
        boat: BoatState,
        objects: Iterable[WorldObject],
    ) -> CollisionReport:
        collisions = []

        boat_x = boat.lane_x
        boat_y = -boat.distance

        for obj in objects:
            if obj.kind not in ("rock",):
                continue

            distance = math.hypot(obj.position.x - boat_x, obj.position.y - boat_y)
            if distance <= self.boat_radius + obj.radius:
                collisions.append(
                    CollisionResult(
                        object_id=obj.object_id,
                        kind=obj.kind,
                        distance=round(distance, 3),
                    )
                )

        return CollisionReport(collisions=tuple(collisions))
