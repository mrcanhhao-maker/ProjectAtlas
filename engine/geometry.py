import math


def point_xy(landmark):
    return landmark.x, landmark.y


def distance(a, b):
    ax, ay = point_xy(a)
    bx, by = point_xy(b)
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def midpoint(a, b):
    ax, ay = point_xy(a)
    bx, by = point_xy(b)
    return (ax + bx) / 2, (ay + by) / 2


def angle(a, b, c):
    ax, ay = point_xy(a)
    bx, by = point_xy(b)
    cx, cy = point_xy(c)

    abx = ax - bx
    aby = ay - by
    cbx = cx - bx
    cby = cy - by

    dot = abx * cbx + aby * cby
    mag_ab = math.sqrt(abx ** 2 + aby ** 2)
    mag_cb = math.sqrt(cbx ** 2 + cby ** 2)

    if mag_ab == 0 or mag_cb == 0:
        return 0

    cos_value = dot / (mag_ab * mag_cb)
    cos_value = max(-1, min(1, cos_value))

    return math.degrees(math.acos(cos_value))
