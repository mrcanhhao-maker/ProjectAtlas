import cv2
import csv
import time
from pathlib import Path

class SessionRecorder:
    def __init__(self, width=640, height=480, fps=20):
        Path("sessions").mkdir(exist_ok=True)
        self.session_id = int(time.time())
        self.video_path = Path("sessions") / f"session_{self.session_id}.mp4"
        self.csv_path = Path("sessions") / f"session_{self.session_id}.csv"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video = cv2.VideoWriter(str(self.video_path), fourcc, fps, (width, height))

        self.csv_file = open(self.csv_path, "w", newline="")
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow([
            "time", "body_angle", "stroke", "spm",
            "power", "distance", "pace", "calories", "state"
        ])

    def write(self, frame, angle, stroke, flywheel):
        self.video.write(frame)
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
        self.video.release()
        self.csv_file.close()
        print(f"Video saved: {self.video_path}")
        print(f"CSV saved: {self.csv_path}")
