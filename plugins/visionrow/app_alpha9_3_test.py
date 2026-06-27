import cv2
import sys
import os
import time
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

from engine.pose_engine import PoseEngine
from engine.pose_features import PoseFeatureExtractor
from engine.stroke_v4 import StrokeEngineV4


def draw_text(frame, text, x, y):
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


def safe_get(data, key, default=0):
    return data.get(key, default)


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Cannot open camera")
        return

    pose_engine = PoseEngine()
    extractor = PoseFeatureExtractor()
    stroke_engine = StrokeEngineV4()

    last_time = time.time()
    start_time = time.time()
    fps = 0
    frames = 0

    confidence_sum = 0
    confidence_count = 0
    max_spm = 0

    print("ProjectAtlas Alpha 9.3 started")
    print("Press Q to quit")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("ERROR: Cannot read frame")
            break

        frames += 1
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

        confidence = safe_get(data, "confidence", 0)
        spm = safe_get(data, "spm", 0)

        confidence_sum += confidence * 100
        confidence_count += 1
        max_spm = max(max_spm, spm)

        quality = min(100, max(0, int(confidence * 0.7 + min(spm, 40) * 0.75)))

        frame = pose_engine.draw(frame, result)

        draw_text(frame, "ProjectAtlas Alpha 9.3 - Confidence + Quality", 20, 40)
        draw_text(frame, f"FPS: {fps}", 20, 80)
        draw_text(frame, f"FSM Phase: {safe_get(data, 'phase', 'None')}", 20, 120)
        draw_text(frame, f"Candidate: {safe_get(data, 'candidate_phase', 'None')}", 20, 160)
        draw_text(frame, f"State Changed: {safe_get(data, 'state_changed', False)}", 20, 200)
        draw_text(frame, f"Stroke: {safe_get(data, 'stroke_count', 0)}", 20, 240)
        draw_text(frame, f"SPM: {spm}", 20, 280)
        draw_text(frame, f"Confidence: {confidence}", 20, 320)
        draw_text(frame, f"Quality: {quality}/100", 20, 360)
        draw_text(frame, f"Back: {safe_get(data, 'back_angle', 0)}", 20, 400)
        draw_text(frame, f"L Elbow: {safe_get(data, 'left_elbow_angle', 0)}", 20, 440)
        draw_text(frame, f"R Elbow: {safe_get(data, 'right_elbow_angle', 0)}", 20, 480)
        draw_text(frame, f"L Knee: {safe_get(data, 'left_knee_angle', 0)}", 20, 520)
        draw_text(frame, f"R Knee: {safe_get(data, 'right_knee_angle', 0)}", 20, 560)

        cv2.imshow("ProjectAtlas Alpha 9.3", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    duration = time.time() - start_time
    avg_confidence = int(confidence_sum / confidence_count) if confidence_count else 0
    final_stroke = safe_get(data, "stroke_count", 0) if "data" in locals() else 0
    avg_spm = round((final_stroke / duration) * 60, 1) if duration > 0 else 0

    session = {
        "version": "Alpha 9.3",
        "duration_sec": round(duration, 1),
        "frames": frames,
        "stroke_count": final_stroke,
        "avg_spm": avg_spm,
        "max_spm": max_spm,
        "avg_confidence": avg_confidence,
    }

    filename = "session_alpha9_3.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)

    print("======== SESSION ========")
    print(f"Duration: {session['duration_sec']} sec")
    print(f"Frames: {session['frames']}")
    print(f"Stroke: {session['stroke_count']}")
    print(f"Average SPM: {session['avg_spm']}")
    print(f"Max SPM: {session['max_spm']}")
    print(f"Average Confidence: {session['avg_confidence']}")
    print(f"Saved: {filename}")
    print("=========================")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
