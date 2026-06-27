import time

class RowingMetrics:
    def __init__(self):
        self.power = 0.0
        self.distance = 0.0
        self.pace_500m = 0.0
        self.calories = 0.0
        self.last_time = time.time()

    def update(self, spm, body_angle):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # Power giả lập v1: đủ để test cảm giác trước
        effort = max(0, min(1, abs(body_angle) / 20))
        self.power = max(0, (spm * 4.5) + (effort * 80))

        # Tốc độ giả lập theo watt
        speed_mps = max(0, (self.power / 120) * 2.2)

        self.distance += speed_mps * dt

        if speed_mps > 0.1:
            self.pace_500m = 500 / speed_mps
        else:
            self.pace_500m = 0

        self.calories += (self.power * dt) / 4184 * 4.0

    def pace_text(self):
        if self.pace_500m <= 0:
            return "--:--"
        m = int(self.pace_500m // 60)
        s = int(self.pace_500m % 60)
        return f"{m}:{s:02d}"
