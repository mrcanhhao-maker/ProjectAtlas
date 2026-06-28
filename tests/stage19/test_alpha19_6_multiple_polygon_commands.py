import numpy as np

from render_queue import PolygonRenderCommand, RenderCommandQueue
from renderer.opencv_polygon_backend import OpenCvPolygonBackend
from renderer.opencv_queue_renderer import OpenCvQueueRenderer


def test_opencv_queue_renderer_draws_multiple_polygon_commands_in_order():
    frame = np.zeros((30, 30, 3), dtype=np.uint8)
    backend = OpenCvPolygonBackend(frame=frame, color=(1, 1, 1))
    renderer = OpenCvQueueRenderer(
        backend,
        layer_colors={
            "river": (10, 20, 30),
            "debug": (40, 50, 60),
        },
    )

    queue = RenderCommandQueue(commands=(
        PolygonRenderCommand(
            layer="river",
            points=((2.0, 2.0), (12.0, 2.0), (12.0, 12.0), (2.0, 12.0)),
        ),
        PolygonRenderCommand(
            layer="debug",
            points=((10.0, 10.0), (20.0, 10.0), (20.0, 20.0), (10.0, 20.0)),
        ),
    ))

    renderer.render(queue)

    assert frame[5, 5].tolist() == [10, 20, 30]
    assert frame[15, 15].tolist() == [40, 50, 60]
    assert frame[11, 11].tolist() == [40, 50, 60]
