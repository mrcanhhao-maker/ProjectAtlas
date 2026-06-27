
import cv2
import time
import mediapipe as mp

from engine.stroke import StrokeDetector
from engine.flywheel import VirtualFlywheel
from engine.calibration import CalibrationEngine
from engine.pose_utils import get_point, midpoint, angle_between_vertical
from engine.recorder import SessionRecorder

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

stroke = StrokeDetector()
flywheel = VirtualFlywheel()
calibration = CalibrationEngine()
recorder = SessionRecorder(width=640, height=480, fps=20)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Khong mo duoc camera")
    exit(1)

prev = time.time()

print("VisionRow Alpha 6.1 dang chay")
print("Q = thoat | R = reset | C = bat/tat calibration")
print("Huong dan: bam C, cheo cham 10 nhip, bam C lan nua de luu calibration")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    now = time.time()
    fps = 1 / max(now - prev, 0.001)
    prev = now

    angle_text = "--"
    skeleton_status = "NOT FOUND"

    if result.pose_landmarks:
        skeleton_status = "FOUND"
        mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        lm = result.pose_landmarks.landmark

        l_shoulder = get_point(lm, mp_pose.PoseLandmark.LEFT_SHOULDER)
        r_shoulder = get_point(lm, mp_pose.PoseLandmark.RIGHT_SHOULDER)
        l_hip = get_point(lm, mp_pose.PoseLandmark.LEFT_HIP)
        r_hip = get_point(lm, mp_pose.PoseLandmark.RIGHT_HIP)

        if l_shoulder and r_shoulder and l_hip and r_hip:
            shoulder_mid = midpoint(l_shoulder, r_shoulder)
            hip_mid = midpoint(l_hip, r_hip)
            angle = angle_between_vertical(shoulder_mid, hip_mid)

            stroke.update(angle)
            calibration.update(stroke.current_angle)
            flywheel.set_calibration_gain(calibration.gain)
            flywheel.update(stroke.current_angle, stroke.spm)

            angle_text = f"{stroke.current_angle:.1f}"
            recorder.write(frame, stroke.current_angle, stroke, flywheel)

    cv2.putText(frame, "VisionRow Alpha 6.1", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255,255,255), 2)
    cv2.putText(frame, f"Skeleton: {skeleton_status}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, f"Body Angle: {angle_text}", (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, f"Stroke: {stroke.count}", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, f"SPM: {stroke.spm:.1f}", (20, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, f"Power: {flywheel.power:.0f} W", (20, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, f"Distance: {flywheel.distance:.1f} m", (20, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, f"Pace 500m: {flywheel.pace_text()}", (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, f"Calories: {flywheel.calories:.1f}", (20, 315), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, f"Calibration: {calibration.status_text()}", (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 385), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255,255,255), 2)
    cv2.putText(frame, "Q quit | R reset | C calibrate", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (255,255,255), 2)

    cv2.imshow("VisionRow Alpha 6.1", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    elif key == ord("r"):
        stroke.reset()
        flywheel.reset()
    elif key == ord("c"):
        if calibration.active:
            ok = calibration.stop()
            if ok:
                flywheel.set_calibration_gain(calibration.gain)
                print(f"Calibration OK. Gain = {calibration.gain:.2f}")
            else:
                print("Calibration failed: can nhieu du lieu hon")
        else:
            calibration.start()
            print("Calibration started. Hay cheo cham 10 nhip, roi bam C lan nua.")

cap.release()
pose.close()
recorder.close()
cv2.destroyAllWindows()
