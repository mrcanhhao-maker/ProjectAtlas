import time


class StrokeEngineV3:
    def __init__(self):
        self.stroke_count = 0
        self.phase = "READY"
        self.last_phase = "READY"
        self.last_stroke_time = time.time()
self.spm = 0
self.min_stroke_interval = 0.8

    def update(self, landmarks):
        if landmarks is None:
            self.phase = "NO BODY"
            return self.data()

        left_wrist = landmarks[15]
        right_wrist = landmarks[16]
        left_hip = landmarks[23]
        right_hip = landmarks[24]

        wrist_y = (left_wrist.y + right_wrist.y) / 2
        hip_y = (left_hip.y + right_hip.y) / 2

        diff = wrist_y - hip_y

        if diff < -0.08:
            self.phase = "FINISH"
        elif diff > 0.12:
            self.phase = "CATCH"
        else:
            self.phase = "DRIVE"

        if self.last_phase == "CATCH" and self.phase == "DRIVE":
    now = time.time()

    if now - self.last_stroke_time > self.min_stroke_interval:
        self.stroke_count += 1

        delta = now - self.last_stroke_time

        if delta > 0:
            self.spm = int(60 / delta)

        self.last_stroke_time = now

        self.last_phase = self.phase
        return self.data()

    def data(self):
        return {
            "phase": self.phase,
            "stroke_count": self.stroke_count,
            "spm": self.spm,
        }
