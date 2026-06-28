from dataclasses import dataclass

from world.camera import TopDownRiverCamera
from world.hud import RiverHud
from world.mission import RiverMission
from world.physics import BoatState, RowingPhysics, StrokeInput
from world.renderer import RenderFrame, RiverRenderer
from world.river_map import RiverMap


@dataclass(frozen=True)
class WorldEngineSnapshot:
    boat: BoatState
    frame: RenderFrame


class RiverWorldEngine:
    def __init__(self, river_map: RiverMap) -> None:
        self.river_map = river_map
        self.physics = RowingPhysics()
        self.camera = TopDownRiverCamera()
        self.mission = RiverMission(river_map)
        self.hud = RiverHud()
        self.renderer = RiverRenderer()
        self.boat = BoatState(lane_x=0.0, distance=0.0, speed=0.0)

    def step(self, stroke: StrokeInput, dt: float) -> WorldEngineSnapshot:
        self.boat = self.physics.step(self.boat, stroke, dt)
        camera_state = self.camera.follow(self.boat)
        mission_state = self.mission.evaluate(self.boat)
        hud_snapshot = self.hud.build(self.boat, mission_state)
        frame = self.renderer.build_frame(self.river_map, camera_state, hud_snapshot)
        return WorldEngineSnapshot(boat=self.boat, frame=frame)
