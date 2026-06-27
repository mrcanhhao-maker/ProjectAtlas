import cv2
import sys
import os
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

from engine.pose_engine import PoseEngine
from engine.pose_features import PoseFeatureExtractor
from engine.stroke_v4 import StrokeEngineV4


def draw_text(frame, text, x, y):
    cv2.putText(
        frame,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Cannot open camera")
        return

    pose_engine = PoseEngine()
    extractor = PoseFeatureExtractor()
    stroke_engine = StrokeEngineV4()

    last_time = time.time()
    fps = 0

    print("ProjectAtlas Alpha 8.2 / Stroke Engine V4.2 FSM started")
    print("Press Q to quit")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("ERROR: Cannot read frame")
            break

        frame = cv2.flip(frame, 1)

        now = time.time()
        delta = now - last_time
        last_time = now
        if delta > 0:
            fps = int(1 / delta)

        result = pose_engine.process(frame)

        landmarks = None
        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

        features = extractor.extract(landmarks)
        data = stroke_engine.update(features)

        frame = pose_engine.draw(frame, result)

        draw_text(frame, "ProjectAtlas Alpha 8.2 - Stroke V4.2 FSM", 20, 40)
        draw_text(frame, f"FPS: {fps}", 20, 80)
        draw_text(frame, f"FSM Phase: {data['phase']}", 20, 120)
        draw_text(frame, f"Candidate: {data['candidate_phase']}", 20, 160)
        draw_text(frame, f"State Changed: {data['state_changed']}", 20, 200)
        draw_text(frame, f"Stroke: {data['stroke_count']}", 20, 240)
        draw_text(frame, f"SPM: {data['spm']}", 20, 280)
        draw_text(frame, f"Confidence: {data['confidence']}", 20, 320)
        draw_text(frame, f"Back: {data['back_angle']}", 20, 360)
        draw_text(frame, f"L Elbow: {data['left_elbow_angle']}", 20, 400)
        draw_text(frame, f"R Elbow: {data['right_elbow_angle']}", 20, 440)
        draw_text(frame, f"L Knee: {data['left_knee_angle']}", 20, 480)
        draw_text(frame, f"R Knee: {data['right_knee_angle']}", 20, 520)

        cv2.imshow("ProjectAtlas Alpha 8.2 Stroke V4.2 FSM", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
