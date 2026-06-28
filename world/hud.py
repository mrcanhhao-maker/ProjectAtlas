from dataclasses import dataclass

from world.mission import MissionState
from world.physics import BoatState


@dataclass(frozen=True)
class HudSnapshot:
    speed: float
    distance: float
    checkpoint: str
    finished: bool


class RiverHud:
    def build(self, boat: BoatState, mission: MissionState) -> HudSnapshot:
        return HudSnapshot(
            speed=round(boat.speed, 2),
            distance=round(boat.distance, 2),
            checkpoint=mission.checkpoint_name,
            finished=mission.finished,
        )
