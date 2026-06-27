import cv2
import sys
import os
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

from engine.pose_engine import PoseEngine
from engine.pose_features import PoseFeatureExtractor
from engine.calibration import CalibrationEngine

pose = PoseEngine()
extractor = PoseFeatureExtractor()
calibration = CalibrationEngine()

cap = cv2.VideoCapture(0)

PHASES = [
    "RECOVERY",
    "CATCH",
    "DRIVE",
    "FINISH"
]

FONT = cv2.FONT_HERSHEY_SIMPLEX

for phase in PHASES:

    countdown = 3

    while countdown > 0:

        ok, frame = cap.read()
        if not ok:
            continue

        frame = cv2.flip(frame,1)

        cv2.putText(frame,f"GET READY : {phase}",(40,60),FONT,1,(0,255,255),2)
        cv2.putText(frame,str(countdown),(250,220),FONT,4,(0,0,255),4)

        cv2.imshow("Calibration",frame)

        cv2.waitKey(1)

        time.sleep(1)

        countdown -= 1

    start=time.time()

    while time.time()-start<3:

        ok,frame=cap.read()

        if not ok:
            continue

        frame=cv2.flip(frame,1)

        result=pose.process(frame)

        if result.pose_landmarks:

            features=extractor.extract(result.pose_landmarks.landmark)

            calibration.add_sample(phase,features)

            frame=pose.draw(frame,result)

        cv2.putText(frame,f"Recording : {phase}",(20,40),FONT,1,(0,255,0),2)

        cv2.imshow("Calibration",frame)

        if cv2.waitKey(1)&0xFF==ord("q"):
            break

calibration.save()

cap.release()
cv2.destroyAllWindows()

print("Calibration Saved")
