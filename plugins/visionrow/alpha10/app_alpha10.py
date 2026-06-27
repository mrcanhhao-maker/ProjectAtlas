from pathlib import Path
import sys
import os
import cv2
import time

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

from engine.pose_engine import PoseEngine
from engine.stroke_v3 import StrokeEngineV3
from engine.quality_engine import QualityEngine
from engine.motion_metrics import MotionMetrics
from engine.stroke_validator import StrokeValidator


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Cannot open camera")
        return

    pose_engine = PoseEngine()
    stroke_engine = StrokeEngineV3()
    quality_engine = QualityEngine()
    motion_metrics = MotionMetrics()
    validator = StrokeValidator()

    print("ProjectAtlas Alpha 10.9 AI Engine started")
    print("Press Q to quit")

    prev_time = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        now = time.time()
        fps = int(1 / (now - prev_time)) if now > prev_time else 0
        prev_time = now

        frame = cv2.flip(frame, 1)

        result = pose_engine.process(frame)

        landmarks = None
        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

        data = stroke_engine.update(landmarks)

        metrics = motion_metrics.update(landmarks)
        data.update(metrics)

        quality = quality_engine.update(data)
        validation = validator.validate(data)

        frame = pose_engine.draw(frame, result)

        rows = [
            f"Phase: {data['phase']}",
            f"Stroke: {data['stroke_count']}",
            f"SPM: {data['spm']}",
            f"FPS: {fps}",
            f"Quality: {quality['quality']}%",
            f"Rhythm: {quality['rhythm']}",
            f"Drive Speed: {metrics['drive_speed']:.2f}",
            f"ROM: {metrics['rom']:.2f}",
            f"VALID: {validation['valid']}",
            f"Reason: {validation['reason']}",
        ]

        y = 40
        cv2.putText(frame,
                    "ProjectAtlas Alpha10.9",
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255,255,255),
                    2)

        for r in rows:
            y += 35

            color = (255,255,255)

            if "VALID" in r:
                color = (0,255,0) if validation["valid"] else (0,0,255)

            cv2.putText(frame,
                        r,
                        (20,y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2)

        cv2.imshow("ProjectAtlas Alpha10.9", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
