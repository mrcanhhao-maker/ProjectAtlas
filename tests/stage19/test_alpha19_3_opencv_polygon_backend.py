import numpy as np

from renderer.opencv_polygon_backend import OpenCvPolygonBackend


def test_opencv_polygon_backend_draws_into_frame():
    frame = np.zeros((20, 20, 3), dtype=np.uint8)

    backend = OpenCvPolygonBackend(
        frame=frame,
        color=(10, 20, 30),
    )

    backend.draw_polygon((
        (5.0, 5.0),
        (15.0, 5.0),
        (15.0, 15.0),
        (5.0, 15.0),
    ))

    assert frame[10, 10].tolist() == [10, 20, 30]
