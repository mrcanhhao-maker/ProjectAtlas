import numpy as np

from render_queue import PolygonRenderCommand, RenderCommandQueue
from renderer.opencv_polygon_backend import OpenCvPolygonBackend
from renderer.opencv_queue_renderer import OpenCvQueueRenderer


def test_opencv_queue_renderer_applies_layer_color_without_geometry_logic():
    frame = np.zeros((20, 20, 3), dtype=np.uint8)
    backend = OpenCvPolygonBackend(frame=frame, color=(1, 1, 1))
    renderer = OpenCvQueueRenderer(
        backend,
        layer_colors={
            "river": (10, 20, 30),
        },
    )

    queue = RenderCommandQueue(commands=(
        PolygonRenderCommand(
            layer="river",
            points=((5.0, 5.0), (15.0, 5.0), (15.0, 15.0), (5.0, 15.0)),
        ),
    ))

    renderer.render(queue)

    assert frame[10, 10].tolist() == [10, 20, 30]
