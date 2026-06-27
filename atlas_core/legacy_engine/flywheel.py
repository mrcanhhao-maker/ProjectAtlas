
import time

class VirtualFlywheel:
    def __init__(self):
        self.velocity = 0.0
        self.power = 0.0
        self.distance = 0.0
        self.calories = 0.0
        self.pace_500m = 0.0
        self.last_time = time.time()
        self.last_angle = None

        self.drag = 0.85
        self.force_gain = 0.008
        self.speed_gain = 0.95
        self.max_speed_mps = 4.0
        self.calibration_gain = 1.0

    def set_calibration_gain(self, gain):
        self.calibration_gain = max(0.5, min(gain, 2.0))

    def update(self, body_angle, spm):
        now = time.time()
        dt = max(now - self.last_time, 0.001)
        self.last_time = now

        if self.last_angle is None:
            self.last_angle = body_angle
            return

        angle_speed = (body_angle - self.last_angle) / dt
        self.last_angle = body_angle

        drive_force = max(0, angle_speed) * self.force_gain * self.calibration_gain

        self.velocity += drive_force
        self.velocity *= max(0.0, 1.0 - self.drag * dt)

        speed_mps = max(0, min(self.velocity * self.speed_gain, self.max_speed_mps))

        raw_power = (speed_mps ** 3) * 4.2 + spm * 2.0
        self.power = max(0, min(raw_power, 450))

        self.distance += speed_mps * dt

        if speed_mps > 0.05:
            self.pace_500m = 500 / speed_mps
        else:
            self.pace_500m = 0

        self.calories += (self.power * dt) / 4184 * 4.0

    def reset(self):
        self.velocity = 0.0
        self.power = 0.0
        self.distance = 0.0
        self.calories = 0.0
        self.pace_500m = 0.0
        self.last_time = time.time()
        self.last_angle = None

    def pace_text(self):
        if self.pace_500m <= 0:
            return "--:--"
        m = int(self.pace_500m // 60)
        s = int(self.pace_500m % 60)
        return f"{m}:{s:02d}"
