import time
from collections import deque

from engine.phase_classifier import PhaseClassifier
from engine.fsm import StrokeFSM


class StrokeEngineV4:
    def __init__(self):
        self.classifier = PhaseClassifier()
        self.fsm = StrokeFSM(confirm_frames=2)

        self.stroke_count = 0
        self.stroke_times = deque(maxlen=5)
        self.spm = 0
        self.last_stroke_time = time.time()
        self.min_stroke_interval = 0.8

        self.current_phase = "UNKNOWN"
        self.score = 0

    def update(self, features):
        if not features or not getattr(features, "body_found", False):
            return self._data(features, "UNKNOWN", "UNKNOWN", False)

        phase, score = self.classifier.classify(features)

        self.current_phase = phase
        self.score = score

        state = self.fsm.update(phase)
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

        return self._data(features, state, phase, self.fsm.state_changed)

    def _data(self, features, state, phase, state_changed):
        confidence = 0
        body_found = False

        if features:
            confidence = getattr(features, "confidence", 0)
            body_found = getattr(features, "body_found", False)

        return {
            "phase": state,
            "candidate_phase": phase,
            "ai_phase": phase,
            "state_changed": state_changed,
            "distance": round(self.score, 2),
            "stroke_count": self.stroke_count,
            "spm": self.spm,
            "body_found": body_found,
            "confidence": round(confidence, 2),
            "back_angle": round(getattr(features, "back_angle", 0), 1) if features else 0,
            "left_elbow_angle": round(getattr(features, "left_elbow_angle", 0), 1) if features else 0,
            "right_elbow_angle": round(getattr(features, "right_elbow_angle", 0), 1) if features else 0,
            "left_knee_angle": round(getattr(features, "left_knee_angle", 0), 1) if features else 0,
            "right_knee_angle": round(getattr(features, "right_knee_angle", 0), 1) if features else 0,
        }
