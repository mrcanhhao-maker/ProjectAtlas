from render_queue import PolygonRenderCommand, RenderCommandQueue
from renderer.opencv_queue_renderer import OpenCvQueueRenderer


class FakeOpenCvBackend:
    def __init__(self):
        self.polygons = []

    def draw_polygon(self, points):
        self.polygons.append(tuple(points))


def test_opencv_queue_renderer_draws_river_polygon_command():
    backend = FakeOpenCvBackend()
    renderer = OpenCvQueueRenderer(backend)

    queue = RenderCommandQueue(commands=(
        PolygonRenderCommand(
            layer="river",
            points=((0.0, 0.0), (1.0, 0.0), (1.0, 1.0)),
        ),
    ))

    renderer.render(queue)

    assert backend.polygons == [
        ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0)),
    ]
