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
from engine.virtual_rower import VirtualRowerEngine

def draw_text(frame, text, x, y):
    import cv2
    cv2.putText(
        frame,
        str(text),
        (int(x), int(y)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )



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
    virtual_rower = VirtualRowerEngine()

    print("ProjectAtlas Alpha 12.4 Virtual Rower Engine started")
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
        data['quality_score'] = float(quality.get('quality', 0)) / 100.0
        rower_data = virtual_rower.update(data)
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
                    "ProjectAtlas Alpha12.4",
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

        draw_text(frame, "Virtual Watts: {}".format(rower_data.get("power_watts", 0)), 20, 320)
        draw_text(frame, "Pace /500m: {}s".format(rower_data.get("pace_500m", 0)), 20, 360)
        draw_text(frame, "Speed: {} m/s".format(rower_data.get("speed_mps", 0)), 20, 400)
        draw_text(frame, "Distance: {} m".format(rower_data.get("distance_m", 0)), 20, 440)
        draw_text(frame, "Moving: {}".format(rower_data.get("is_moving", False)), 20, 480)
        cv2.imshow("ProjectAtlas Alpha12.4", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
