import time
from collections import deque

from engine.phase_detector import PhaseDetector
from engine.fsm import StrokeFSM


class StrokeEngineV4:
    def __init__(self):
        self.detector = PhaseDetector()
        self.fsm = StrokeFSM(confirm_frames=3)

        self.stroke_count = 0
        self.stroke_times = deque(maxlen=5)
        self.spm = 0

        self.last_stroke_time = time.time()
        self.min_stroke_interval = 0.8

        self.candidate_phase = "UNKNOWN"

    def update(self, features):
        self.candidate_phase = self.detector.detect(features)
        phase = self.fsm.update(self.candidate_phase)

        now = time.time()

        if self.fsm.completed_stroke:
            if now - self.last_stroke_time > self.min_stroke_interval:
                self.stroke_count += 1
                self.stroke_times.append(now)

                if len(self.stroke_times) >= 2:
                    duration = self.stroke_times[-1] - self.stroke_times[0]
                    strokes = len(self.stroke_times) - 1
                    if duration > 0:
                        self.spm = int((strokes / duration) * 60)

                self.last_stroke_time = now

        return self.data(features, phase)

    def data(self, features, phase):
        return {
            "phase": phase,
            "candidate_phase": self.candidate_phase,
            "state_changed": self.fsm.state_changed,
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
