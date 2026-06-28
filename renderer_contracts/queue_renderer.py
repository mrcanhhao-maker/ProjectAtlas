from typing import Protocol

from render_queue import RenderCommandQueue


class QueueRendererContract(Protocol):
    """
    Renderer backend contract.

    OpenCV, Unity, Metal, OpenGL, Android and iOS renderers
    should consume only RenderCommandQueue.
    """

    def render(self, queue: RenderCommandQueue) -> None:
        ...
