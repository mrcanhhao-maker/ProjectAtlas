import time
from collections import deque

class StrokeDetector:
    def __init__(self):
        self.count = 0
        self.spm = 0.0
        self.state = "READY"
        self.values = deque(maxlen=5)
        self.stroke_times = deque(maxlen=8)
        self.last_stroke_time = 0
        self.min_interval = 0.35
        self.forward_threshold = -2.0
        self.back_threshold = 2.0
        self.current_angle = 0.0

    def smooth(self, value):
        self.values.append(value)
        return sum(self.values) / len(self.values)

    def update(self, raw_angle):
        now = time.time()
        angle = self.smooth(raw_angle)
        self.current_angle = angle

        if self.state == "READY":
            if angle <= self.forward_threshold:
                self.state = "FORWARD"
            elif angle >= self.back_threshold:
                self.state = "BACK"

        elif self.state == "FORWARD":
            if angle >= self.back_threshold and now - self.last_stroke_time >= self.min_interval:
                self.count += 1
                self.last_stroke_time = now
                self.stroke_times.append(now)
                self.state = "BACK"
                self._calculate_spm()

        elif self.state == "BACK":
            if angle <= self.forward_threshold:
                self.state = "FORWARD"

    def reset(self):
        self.count = 0
        self.spm = 0.0
        self.state = "READY"
        self.values.clear()
        self.stroke_times.clear()
        self.last_stroke_time = 0
        self.current_angle = 0.0

    def _calculate_spm(self):
        if len(self.stroke_times) >= 2:
            duration = self.stroke_times[-1] - self.stroke_times[0]
            strokes = len(self.stroke_times) - 1
            if duration > 0:
                self.spm = strokes / duration * 60
