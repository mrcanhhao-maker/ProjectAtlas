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
        drive_speed = float(data.get("drive_speed", 0.0))
        rom = float(data.get("rom", 0.0))

        score = 0

        score += confidence * 25

        if phase in ("CATCH", "DRIVE", "FINISH", "RECOVERY"):
            score += 20

        if state_changed:
            score += 15

        if stroke_count > 0:
            score += 10

        score += min(drive_speed * 2, 15)
        score += min(rom * 2, 15)

        score = int(self.clamp(score))
        self.history.append(score)

        rhythm = sum(self.history) / len(self.history) if self.history else 0

        return {
            "quality": score,
            "rhythm": round(rhythm, 1),
            "drive_speed": drive_speed,
            "rom": rom,
            "confidence": confidence,
            "state_changed": state_changed,
            "phase_valid": phase in ("CATCH", "DRIVE", "FINISH", "RECOVERY"),
        }
