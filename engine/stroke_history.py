from collections import deque
import time

class StrokeHistory:
    def __init__(self, maxlen=20):
        self.strokes = deque(maxlen=maxlen)
        self.last_stroke_count = 0

    def update(self, data, quality, validation):
        stroke_count = int(data.get("stroke_count", 0))

        new_stroke = stroke_count > self.last_stroke_count

        if new_stroke:
            item = {
                "time": time.time(),
                "stroke": stroke_count,
                "phase": data.get("phase", "UNKNOWN"),
                "spm": data.get("spm", 0),
                "quality": quality.get("quality", 0),
                "rhythm": quality.get("rhythm", 0),
                "drive_speed": data.get("drive_speed", 0),
                "rom": data.get("rom", 0),
                "valid": validation.get("valid", False),
                "reason": validation.get("reason", "UNKNOWN"),
            }
            self.strokes.append(item)

        self.last_stroke_count = stroke_count

        return {
            "new_stroke": new_stroke,
            "total_saved": len(self.strokes),
            "last": self.strokes[-1] if self.strokes else None,
            "avg_quality": self.average_quality(),
        }

    def average_quality(self):
        if not self.strokes:
            return 0
        return round(sum(s["quality"] for s in self.strokes) / len(self.strokes), 1)
