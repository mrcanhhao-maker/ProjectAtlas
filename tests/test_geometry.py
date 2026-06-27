import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from engine.geometry import angle


class P:
    def __init__(self, x, y):
        self.x = x
        self.y = y


a = P(0, 0)
b = P(1, 0)
c = P(1, 1)

ang = angle(a, b, c)

assert abs(ang - 90) < 0.01

print("Geometry Test PASS")
