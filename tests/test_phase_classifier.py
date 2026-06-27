import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from engine.phase_classifier import PhaseClassifier


class F:

    wrist_to_hip = -0.25

    back_angle = 33

    left_elbow_angle = 143
    right_elbow_angle = 161

    left_knee_angle = 80
    right_knee_angle = 86


clf = PhaseClassifier()

phase, score = clf.classify(F())

print("Phase :", phase)
print("Score :", round(score,2))

assert phase == "CATCH"

print("PHASE CLASSIFIER PASS")
