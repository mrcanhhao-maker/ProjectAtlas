from render_queue import RenderCommandQueue
from renderer_contracts import QueueRendererContract


class OpenCvQueueRenderer(QueueRendererContract):
    def __init__(self, backend):
        self._backend = backend

    def render(self, queue: RenderCommandQueue) -> None:
        if hasattr(self._backend, "render_queue"):
            self._backend.render_queue(queue)
            return

        raise NotImplementedError(
            "Backend must implement render_queue(RenderCommandQueue)"
        )
