import cv2
import sys
import os
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

from engine.pose_engine import PoseEngine
from engine.pose_features import PoseFeatureExtractor
from engine.stroke_v4 import StrokeEngineV4


def draw_text(frame, text, x, y, color=(255, 255, 255)):
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


def main():
    cap = cv2.VideoCapture(0)
    pose_engine = PoseEngine()
    extractor = PoseFeatureExtractor()
    stroke_engine = StrokeEngineV4()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)
        result = pose_engine.process(frame)

        landmarks = result.pose_landmarks.landmark if result.pose_landmarks else None
        features = extractor.extract(landmarks)
        data = stroke_engine.update(features)

        frame = pose_engine.draw(frame, result)

        draw_text(frame, "Alpha 9.3 DEBUG", 20, 40)
        draw_text(frame, f"Body Found: {features.body_found}", 20, 90)
        draw_text(frame, f"Confidence: {features.confidence:.3f}", 20, 130)
        draw_text(frame, f"AI Phase: {data['ai_phase']}", 20, 170)
        draw_text(frame, f"FSM Phase: {data['phase']}", 20, 210)
        draw_text(frame, f"State Changed: {data['state_changed']}", 20, 250)
        draw_text(frame, f"Stroke: {data['stroke_count']}", 20, 290)
        draw_text(frame, f"SPM: {data['spm']}", 20, 330)
        draw_text(frame, f"Wrist-Hip: {features.wrist_to_hip:.3f}", 20, 370)
        draw_text(frame, f"Back: {features.back_angle:.1f}", 20, 410)
        draw_text(frame, f"L Knee: {features.left_knee_angle:.1f}", 20, 450)
        draw_text(frame, f"R Knee: {features.right_knee_angle:.1f}", 20, 490)

        cv2.imshow("ProjectAtlas Alpha 9.3 DEBUG", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
