from dataclasses import dataclass

from world.camera import CameraState
from typing import Tuple

from world.hud import HudSnapshot
from world.objects import VisibleObject
from world.river_map import RiverMap


@dataclass(frozen=True)
class RenderFrame:
    world_name: str
    camera_y: float
    visible_objects: Tuple[VisibleObject, ...]
    hud: HudSnapshot


class RiverRenderer:
    def build_frame(
        self,
        river_map: RiverMap,
        camera: CameraState,
        hud: HudSnapshot,
        visible_objects: Tuple[VisibleObject, ...] = (),
    ) -> RenderFrame:
        return RenderFrame(
            world_name=river_map.name,
            camera_y=camera.y,
            visible_objects=visible_objects,
            hud=hud,
        )
