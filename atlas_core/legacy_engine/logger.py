import csv
import time
from pathlib import Path

class SessionLogger:
    def __init__(self):
        Path("logs").mkdir(exist_ok=True)
        self.path = Path("logs") / f"session_{int(time.time())}.csv"
        self.file = open(self.path, "w", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            "time", "body_angle", "stroke", "spm",
            "power", "distance", "pace", "calories", "state"
        ])

    def log(self, angle, stroke, flywheel):
        self.writer.writerow([
            time.time(),
            angle,
            stroke.count,
            stroke.spm,
            flywheel.power,
            flywheel.distance,
            flywheel.pace_500m,
            flywheel.calories,
            stroke.state
        ])

    def close(self):
        self.file.close()
        print(f"Log saved: {self.path}")
