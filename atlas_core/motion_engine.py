from collections import deque
import time

class MotionEngineV2:
    def __init__(self):
        self.state = "READY"
        self.stroke_count = 0
        self.spm = 0.0
        self.angle_history = deque(maxlen=8)
        self.stroke_times = deque(maxlen=6)
        self.last_time = time.time()
        self.last_angle = None
        self.velocity = 0.0
        self.lost_frames = 0
        self.max_lost_frames = 5

    def update(self, angle, skeleton_found=True):
        now = time.time()

        if not skeleton_found:
            self.lost_frames += 1
            if self.lost_frames <= self.max_lost_frames:
                return
            self.state = "TRACK_LOST"
            return

        self.lost_frames = 0

        if angle is None:
            return

        self.angle_history.append(angle)
        smooth_angle = sum(self.angle_history) / len(self.angle_history)

        if self.last_angle is None:
            self.last_angle = smooth_angle
            self.last_time = now
            return

        dt = max(now - self.last_time, 0.001)
        self.velocity = (smooth_angle - self.last_angle) / dt

        self.last_angle = smooth_angle
        self.last_time = now

        self._state_machine(smooth_angle, self.velocity, now)

    def _state_machine(self, angle, velocity, now):
        if self.state in ["READY", "TRACK_LOST"]:
            if velocity < -15:
                self.state = "CATCH"

        elif self.state == "CATCH":
            if velocity > 20:
                self.state = "DRIVE"

        elif self.state == "DRIVE":
            if velocity < 5 and angle > 3:
                self.state = "FINISH"
                self._add_stroke(now)

        elif self.state == "FINISH":
            if velocity < -10:
                self.state = "RECOVERY"

        elif self.state == "RECOVERY":
            if velocity > 10:
                self.state = "DRIVE"

    def _add_stroke(self, now):
        if self.stroke_times and now - self.stroke_times[-1] < 0.55:
            return

        self.stroke_count += 1
        self.stroke_times.append(now)

        if len(self.stroke_times) >= 2:
            duration = self.stroke_times[-1] - self.stroke_times[0]
            strokes = len(self.stroke_times) - 1
            if duration > 0:
                self.spm = strokes / duration * 60

    def reset(self):
        self.state = "READY"
        self.stroke_count = 0
        self.spm = 0.0
        self.angle_history.clear()
        self.stroke_times.clear()
        self.last_angle = None
        self.velocity = 0.0
        self.lost_frames = 0
