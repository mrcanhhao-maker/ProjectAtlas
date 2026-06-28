from dataclasses import dataclass

from world.physics import BoatState
from world.river_map import RiverMap


@dataclass(frozen=True)
class MissionState:
    checkpoint_name: str
    finished: bool


class RiverMission:
    def __init__(self, river_map: RiverMap) -> None:
        if not river_map.checkpoints:
            raise ValueError("river map must have checkpoints")
        self.river_map = river_map

    def evaluate(self, boat: BoatState) -> MissionState:
        current = self.river_map.checkpoints[0]
        for checkpoint in self.river_map.checkpoints:
            if boat.distance >= abs(checkpoint.position.y):
                current = checkpoint

        finish = self.river_map.checkpoints[-1]
        return MissionState(
            checkpoint_name=current.name,
            finished=current.name == finish.name,
        )
