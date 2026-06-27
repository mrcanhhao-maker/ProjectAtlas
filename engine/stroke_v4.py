import time
from collections import deque


class StrokeEngineV4:
    def __init__(self):
        self.phase = "READY"
        self.last_phase = "READY"

        self.stroke_count = 0
        self.last_stroke_time = time.time()
        self.min_stroke_interval = 0.8

        self.stroke_times = deque(maxlen=5)
        self.spm = 0

    def update(self, features):
        if not features.body_found or features.confidence < 0.35:
            self.phase = "NO BODY"
            return self.data(features)

        diff = features.wrist_to_hip

        if diff > 0.12:
            self.phase = "CATCH"
        elif diff < -0.08:
            self.phase = "FINISH"
        else:
            self.phase = "DRIVE"

        now = time.time()

        if self.last_phase == "FINISH" and self.phase == "CATCH":
            if now - self.last_stroke_time > self.min_stroke_interval:
                self.stroke_count += 1
                self.stroke_times.append(now)

                if len(self.stroke_times) >= 2:
                    duration = self.stroke_times[-1] - self.stroke_times[0]
                    strokes = len(self.stroke_times) - 1
                    if duration > 0:
                        self.spm = int((strokes / duration) * 60)

                self.last_stroke_time = now

        self.last_phase = self.phase

        return self.data(features)

    def data(self, features):
        return {
            "phase": self.phase,
            "last_phase": self.last_phase,
            "stroke_count": self.stroke_count,
            "spm": self.spm,
            "body_found": features.body_found,
            "confidence": round(features.confidence, 2),
            "back_angle": int(features.back_angle),
            "left_elbow_angle": int(features.left_elbow_angle),
            "right_elbow_angle": int(features.right_elbow_angle),
            "left_knee_angle": int(features.left_knee_angle),
            "right_knee_angle": int(features.right_knee_angle),
        }
