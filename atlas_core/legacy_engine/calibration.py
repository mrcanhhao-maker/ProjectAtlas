
class CalibrationEngine:
    def __init__(self):
        self.active = False
        self.values = []
        self.min_angle = None
        self.max_angle = None
        self.gain = 1.0

    def start(self):
        self.active = True
        self.values = []
        self.min_angle = None
        self.max_angle = None
        self.gain = 1.0

    def stop(self):
        self.active = False
        if len(self.values) < 10:
            return False

        self.min_angle = min(self.values)
        self.max_angle = max(self.values)
        amplitude = abs(self.max_angle - self.min_angle)

        if amplitude < 8:
            self.gain = 1.4
        elif amplitude > 28:
            self.gain = 0.75
        else:
            self.gain = 18 / amplitude

        self.gain = max(0.5, min(self.gain, 2.0))
        return True

    def update(self, angle):
        if self.active:
            self.values.append(angle)

    def status_text(self):
        if self.active:
            return f"CALIBRATING {len(self.values)}"
        if self.min_angle is None:
            return "NOT SET"
        return f"OK gain={self.gain:.2f}"
