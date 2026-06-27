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


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Cannot open camera")
        return

    pose_engine = PoseEngine()
    stroke_engine = StrokeEngineV3()
    quality_engine = QualityEngine()

    print("ProjectAtlas Alpha 10.2 AI Engine started")
    print("Press Q to quit")

    prev_time = time.time()

    while True:
        ok, frame = cap.read()
        now = time.time()
        fps = int(1 / (now - prev_time)) if now > prev_time else 0
        prev_time = now

        if not ok:
            print("ERROR: Cannot read frame")
            break

        frame = cv2.flip(frame, 1)
        result = pose_engine.process(frame)

        landmarks = None
        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

        data = stroke_engine.update(landmarks)
        confidence = data.get("confidence", 0.0)
        state_changed = data.get("state_changed", False)
        quality = quality_engine.update(data)

        frame = pose_engine.draw(frame, result)

        cv2.putText(frame, "ProjectAtlas Alpha 10.2 AI", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(frame, f"Phase: {data['phase']}", (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.putText(frame, f"Stroke: {data['stroke_count']}", (20, 135),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.putText(frame, f"SPM: {data['spm']}", (20, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.putText(frame, f"FPS: {fps}", (20, 225),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.putText(frame, f"Confidence: {confidence:.2f}", (20, 270),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.putText(frame, f"Changed: {state_changed}", (20, 315),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        cv2.putText(frame, f"Quality: {quality['quality']}%", (20, 360),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

        cv2.imshow("ProjectAtlas Alpha 10.2 AI Test", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
