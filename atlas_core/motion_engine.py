from collections import deque
import time

class MotionEngineV2:
    def __init__(self):
        self.state = "READY"
        self.stroke_count = 0
        self.spm = 0.0
        self.angle_history = deque(maxlen=5)
        self.stroke_times = deque(maxlen=8)
        self.last_angle = None
        self.last_time = time.time()
        self.velocity = 0.0
        self.min_interval = 0.45
        self.last_stroke_time = 0
        self.forward_seen = False
        self.back_seen = False

    def update(self, angle, skeleton_found=True):
        if not skeleton_found or angle is None:
            return

        now = time.time()
        self.angle_history.append(angle)
        a = sum(self.angle_history) / len(self.angle_history)

        if self.last_angle is None:
            self.last_angle = a
            self.last_time = now
            return

        dt = max(now - self.last_time, 0.001)
        self.velocity = (a - self.last_angle) / dt
        self.last_angle = a
        self.last_time = now

        # Pha cúi người / recovery
        if a < -4:
            self.forward_seen = True
            self.state = "CATCH"

        # Pha ngả/kéo về
        if self.forward_seen and a > 4:
            self.back_seen = True
            self.state = "DRIVE"

        # Hoàn thành 1 stroke khi đã đi từ cúi -> ngả
        if self.forward_seen and self.back_seen and now - self.last_stroke_time > self.min_interval:
            self.stroke_count += 1
            self.last_stroke_time = now
            self.stroke_times.append(now)
            self.state = "FINISH"
            self.forward_seen = False
            self.back_seen = False
            self._calc_spm()

        if self.state == "FINISH" and a < 0:
            self.state = "RECOVERY"

    def _calc_spm(self):
        if len(self.stroke_times) >= 2:
            duration = self.stroke_times[-1] - self.stroke_times[0]
            strokes = len(self.stroke_times) - 1
            if duration > 0:
                self.spm = strokes / duration * 60

    def reset(self):
        self.__init__()
