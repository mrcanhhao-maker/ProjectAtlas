from render_queue import PolygonRenderCommand, RenderCommandQueue
from renderer_contracts import QueueRendererContract


class FakeQueueRenderer:
    def __init__(self):
        self.last_queue = None

    def render(self, queue: RenderCommandQueue) -> None:
        self.last_queue = queue


def test_renderer_contract_consumes_only_render_command_queue():
    renderer: QueueRendererContract = FakeQueueRenderer()

    queue = RenderCommandQueue(commands=(
        PolygonRenderCommand(
            layer="river",
            points=((0.0, 0.0), (1.0, 1.0), (2.0, 0.0)),
        ),
    ))

    renderer.render(queue)

    assert renderer.last_queue is queue
