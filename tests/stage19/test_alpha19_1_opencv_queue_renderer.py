from render_queue import PolygonRenderCommand, RenderCommandQueue
from renderer.opencv_queue_renderer import OpenCvQueueRenderer


class FakeBackend:
    def __init__(self):
        self.queue = None

    def render_queue(self, queue):
        self.queue = queue


def test_opencv_queue_renderer_forwards_render_queue():
    backend = FakeBackend()
    renderer = OpenCvQueueRenderer(backend)

    queue = RenderCommandQueue(
        commands=(
            PolygonRenderCommand(
                layer="river",
                points=((0.0, 0.0), (1.0, 0.0), (1.0, 1.0)),
            ),
        )
    )

    renderer.render(queue)

    assert backend.queue is queue
