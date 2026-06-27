from collections import deque

class QualityEngine:
    def __init__(self):
        self.history = deque(maxlen=10)

    def clamp(self, value, low=0, high=100):
        return max(low, min(high, value))

    def update(self, data):
        confidence = float(data.get("confidence", 0.0))
        state_changed = bool(data.get("state_changed", False))
        phase = data.get("phase", "UNKNOWN")
        stroke_count = int(data.get("stroke_count", 0))

        score = 0

        # 40 điểm: confidence
        score += confidence * 40

        # 20 điểm: phase hợp lệ
        if phase in ("CATCH", "DRIVE", "FINISH", "RECOVERY"):
            score += 20

        # 20 điểm: có đổi trạng thái
        if state_changed:
            score += 20

        # 20 điểm: đã phát hiện stroke
        if stroke_count > 0:
            score += 20

        score = int(self.clamp(score))
        self.history.append(score)

        rhythm = sum(self.history) / len(self.history) if self.history else 0

        return {
            "quality": score,
            "rhythm": round(rhythm, 1),
            "confidence": confidence,
            "state_changed": state_changed,
            "phase_valid": phase in ("CATCH", "DRIVE", "FINISH", "RECOVERY"),
        }
