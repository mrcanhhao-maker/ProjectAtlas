from typing import Mapping, Tuple

from render_queue import RenderCommandQueue
from renderer_contracts import QueueRendererContract


Color = Tuple[int, int, int]


class OpenCvQueueRenderer(QueueRendererContract):
    def __init__(
        self,
        backend,
        layer_colors: Mapping[str, Color] | None = None,
    ):
        self._backend = backend
        self._layer_colors = dict(layer_colors or {})

    def render(self, queue: RenderCommandQueue) -> None:
        for command in queue.commands:
            if command.layer == "river":
                color = self._layer_colors.get(command.layer)
                if color is None:
                    self._backend.draw_polygon(command.points)
                else:
                    self._backend.draw_polygon(command.points, color=color)
