from dataclasses import dataclass

from world.camera import CameraState
from world.hud import HudSnapshot
from world.river_map import RiverMap


@dataclass(frozen=True)
class RenderFrame:
    world_name: str
    camera_y: float
    hud: HudSnapshot


class RiverRenderer:
    def build_frame(
        self,
        river_map: RiverMap,
        camera: CameraState,
        hud: HudSnapshot,
    ) -> RenderFrame:
        return RenderFrame(
            world_name=river_map.name,
            camera_y=camera.y,
            hud=hud,
        )
