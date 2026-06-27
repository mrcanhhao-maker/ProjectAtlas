class QualityEngine:
    def __init__(self):
        self.score = 0

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
        if phase in ["CATCH", "DRIVE", "FINISH", "RECOVERY"]:
            score += 20

        # 20 điểm: có chuyển trạng thái
        if state_changed:
            score += 20

        # 20 điểm: đã phát hiện stroke
        if stroke_count > 0:
            score += 20

        self.score = int(self.clamp(score))

        return {
            "quality": self.score,
            "confidence": confidence,
            "phase_valid": phase in ["CATCH", "DRIVE", "FINISH", "RECOVERY"],
            "state_changed": state_changed,
        }
