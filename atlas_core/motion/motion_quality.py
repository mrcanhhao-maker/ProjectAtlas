from collections import deque
import math


class MotionQuality:

    def __init__(self, history_size=10):
        self.history = deque(maxlen=history_size)
        self.prev_point = None
        self.prev_velocity = 0.0
        self.max_velocity = 0.0

    def update(self, point):

        empty = {
            "velocity": 0.0,
            "acceleration": 0.0,
            "distance": 0.0,
            "max_velocity": self.max_velocity,
            "dx": 0.0,
            "dy": 0.0,
            "direction_x": "NONE",
            "direction_y": "NONE",
            "motion_state": "STOP",
        }

        if point is None:
            return empty

        if self.prev_point is None:
            self.prev_point = point
            return empty

        dx = point[0] - self.prev_point[0]
        dy = point[1] - self.prev_point[1]

        distance = math.sqrt(dx * dx + dy * dy)
        velocity = distance
        acceleration = velocity - self.prev_velocity

        if velocity > self.max_velocity:
            self.max_velocity = velocity

        if dx > 0:
            direction_x = "RIGHT"
        elif dx < 0:
            direction_x = "LEFT"
        else:
            direction_x = "NONE"

        if dy > 0:
            direction_y = "DOWN"
        elif dy < 0:
            direction_y = "UP"
        else:
            direction_y = "NONE"

        if velocity < 0.02:
            motion_state = "STOP"
        elif direction_x == "LEFT":
            motion_state = "DRIVE"
        elif direction_x == "RIGHT":
            motion_state = "RECOVERY"
        else:
            motion_state = "UNKNOWN"

        self.prev_velocity = velocity
        self.prev_point = point
        self.history.append(velocity)

        return {
            "velocity": velocity,
            "acceleration": acceleration,
            "distance": distance,
            "max_velocity": self.max_velocity,
            "dx": dx,
            "dy": dy,
            "direction_x": direction_x,
            "direction_y": direction_y,
            "motion_state": motion_state,
        }
