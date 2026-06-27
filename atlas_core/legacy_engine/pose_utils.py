
import math

def get_point(landmarks, landmark_enum, min_visibility=0.45):
    p = landmarks[landmark_enum.value]
    if p.visibility < min_visibility:
        return None
    return (p.x, p.y)

def midpoint(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

def angle_between_vertical(top, bottom):
    dx = top[0] - bottom[0]
    dy = top[1] - bottom[1]
    return math.degrees(math.atan2(dx, -dy))
