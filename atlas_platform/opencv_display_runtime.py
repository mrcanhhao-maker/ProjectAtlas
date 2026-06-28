from dataclasses import dataclass

import cv2

from atlas_platform.runtime_contract import RuntimeFrame
from renderer.opencv_world_renderer import OpenCVWorldRenderer
from renderer.world_scene_adapter import BoatSnapshot


@dataclass
class OpenCVDisplayRuntime:
    renderer: OpenCVWorldRenderer
    window_name: str = "ProjectAtlas Alpha 16"

    def present(self, frame: RuntimeFrame) -> None:
        image = self.renderer.render_queue(
            frame.render_queue,
            BoatSnapshot(x=frame.boat_x, y=frame.boat_y),
        )
        cv2.imshow(self.window_name, image)
