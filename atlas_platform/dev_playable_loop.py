from dataclasses import dataclass
from time import perf_counter, sleep

import cv2

from atlas_platform.core_runtime import CoreRuntime
from atlas_platform.opencv_display_runtime import OpenCVDisplayRuntime


@dataclass
class DevPlayableLoop:
    runtime: CoreRuntime
    display: OpenCVDisplayRuntime
    target_fps: int = 60
    exit_key: int = 27

    def __post_init__(self):
        if self.target_fps <= 0:
            raise ValueError("target_fps must be positive")

    def run(self) -> None:
        previous = perf_counter()
        target_dt = 1.0 / self.target_fps

        while True:
            now = perf_counter()
            dt = now - previous
            previous = now

            frame = self.runtime.update(dt)
            self.display.present(frame)

            key = cv2.waitKey(1) & 0xFF
            if key == self.exit_key:
                break

            elapsed = perf_counter() - now
            remaining = target_dt - elapsed
            if remaining > 0:
                sleep(remaining)

        cv2.destroyAllWindows()
