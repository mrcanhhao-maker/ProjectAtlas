import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from engine.calibration_wizard import CalibrationWizard


class Feature:

    body_found = True

    wrist_to_hip = 0.1
    back_angle = 82

    left_elbow_angle = 145
    right_elbow_angle = 145

    left_knee_angle = 95
    right_knee_angle = 95


def provider():
    return Feature()


wizard = CalibrationWizard()

wizard.run(provider)

print("AUTO CALIBRATION TEST PASS")
