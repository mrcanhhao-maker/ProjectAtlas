import math

class MotionMetrics:
    def __init__(self):
        self.prev_shoulder = None
        self.drive_speed = 0.0
        self.rom = 0.0

    def update(self, landmarks):
        if landmarks is None:
            return {
                "drive_speed": 0.0,
                "rom": self.rom
            }

        left = landmarks[11]
        right = landmarks[12]

        shoulder_x = (left.x + right.x) / 2.0

        if self.prev_shoulder is not None:
            self.drive_speed = abs(shoulder_x - self.prev_shoulder)

        self.prev_shoulder = shoulder_x

        self.rom = max(self.rom, self.drive_speed)

        return {
            "drive_speed": round(self.drive_speed * 1000, 2),
            "rom": round(self.rom * 1000, 2)
        }
