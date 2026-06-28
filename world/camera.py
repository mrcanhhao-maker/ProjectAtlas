from dataclasses import dataclass

from world.physics import BoatState


@dataclass(frozen=True)
class CameraState:
    x: float
    y: float
    boat_screen_y: float


class TopDownRiverCamera:
    def __init__(self, boat_screen_y: float = 0.78) -> None:
        if not 0.5 <= boat_screen_y <= 0.95:
            raise ValueError("boat_screen_y must keep boat near bottom of screen")
        self.boat_screen_y = boat_screen_y

    def follow(self, boat: BoatState) -> CameraState:
        return CameraState(
            x=boat.lane_x,
            y=-boat.distance,
            boat_screen_y=self.boat_screen_y,
        )
