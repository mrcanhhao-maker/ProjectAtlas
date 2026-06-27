import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from engine.calibration import CalibrationEngine


class F:

    wrist_to_hip = 0.15

    back_angle = 82

    left_elbow_angle = 145

    right_elbow_angle = 144

    left_knee_angle = 92

    right_knee_angle = 94


cal = CalibrationEngine()

for i in range(10):
    cal.add_sample("CATCH", F())

profile = cal.build_profile()

assert abs(profile["CATCH"]["wrist_to_hip"] - 0.15) < 0.001

print(profile)

cal.save()

print("CALIBRATION TEST PASS")
