from typing import Tuple

import cv2
import numpy as np


Point = Tuple[float, float]
Color = Tuple[int, int, int]


class OpenCvPolygonBackend:
    """
    Minimal OpenCV polygon backend.

    It knows how to draw polygons, but it does not know river geometry.
    """

    def __init__(self, frame, color: Color = (80, 120, 180)):
        self.frame = frame
        self.color = color

    def draw_polygon(self, points: tuple[Point, ...]) -> None:
        pts = np.array(
            [[int(round(x)), int(round(y))] for x, y in points],
            dtype=np.int32,
        )
        cv2.fillPoly(self.frame, [pts], self.color)
