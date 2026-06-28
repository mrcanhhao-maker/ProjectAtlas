from dataclasses import dataclass
from typing import Protocol

from renderer.render_queue import RenderQueue


@dataclass(frozen=True)
class RuntimeFrame:
    render_queue: RenderQueue
    boat_x: float
    boat_y: float
    fps: float = 0.0


class WorldRuntime(Protocol):
    def update(self, dt: float) -> RuntimeFrame:
        ...


class DisplayRuntime(Protocol):
    def present(self, frame: RuntimeFrame) -> None:
        ...
