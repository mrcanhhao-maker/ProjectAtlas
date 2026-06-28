from render_queue import RenderCommandQueue
from renderer_contracts import QueueRendererContract


class OpenCvQueueRenderer(QueueRendererContract):
    def __init__(self, backend):
        self._backend = backend

    def render(self, queue: RenderCommandQueue) -> None:
        for command in queue.commands:
            if command.layer == "river":
                self._backend.draw_polygon(command.points)
