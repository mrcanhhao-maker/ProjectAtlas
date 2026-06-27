import cv2
import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

from engine.pose_engine import PoseEngine
from engine.stroke_v3 import StrokeEngineV3


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Cannot open camera")
        return

    pose_engine = PoseEngine()
    stroke_engine = StrokeEngineV3()

    print("ProjectAtlas Alpha 8 started")
    print("Press Q to quit")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("ERROR: Cannot read frame")
            break

        frame = cv2.flip(frame, 1)

        result = pose_engine.process(frame)

        landmarks = None
        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

        data = stroke_engine.update(landmarks)

        frame = pose_engine.draw(frame, result)

        cv2.putText(frame, "ProjectAtlas Alpha 8", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(frame, f"Phase: {data['phase']}", (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.putText(frame, f"Stroke: {data['stroke_count']}", (20, 135),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.putText(frame, f"SPM: {data['spm']}", (20, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("ProjectAtlas Alpha 8 Test", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
