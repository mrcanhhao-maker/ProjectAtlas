import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from engine.pose_features import PoseFeatureExtractor


class Landmark:
    def __init__(self, x, y, visibility=1.0):
        self.x = x
        self.y = y
        self.visibility = visibility


# tạo 33 landmark giả
landmarks = [Landmark(0.5, 0.5) for _ in range(33)]

# Shoulder
landmarks[11] = Landmark(0.40, 0.30)
landmarks[12] = Landmark(0.60, 0.30)

# Elbow
landmarks[13] = Landmark(0.40, 0.45)
landmarks[14] = Landmark(0.60, 0.45)

# Wrist
landmarks[15] = Landmark(0.40, 0.60)
landmarks[16] = Landmark(0.60, 0.60)

# Hip
landmarks[23] = Landmark(0.42, 0.60)
landmarks[24] = Landmark(0.58, 0.60)

# Knee
landmarks[25] = Landmark(0.42, 0.80)
landmarks[26] = Landmark(0.58, 0.80)

# Ankle
landmarks[27] = Landmark(0.42, 1.00)
landmarks[28] = Landmark(0.58, 1.00)

extractor = PoseFeatureExtractor()
features = extractor.extract(landmarks)

assert features.body_found
assert features.confidence > 0.9
assert features.shoulder_width > 0

print("===== POSE FEATURE TEST =====")
print("Confidence :", features.confidence)
print("Shoulder Width :", round(features.shoulder_width,3))
print("Back Angle :", round(features.back_angle,1))
print("Left Elbow :", round(features.left_elbow_angle,1))
print("Right Elbow :", round(features.right_elbow_angle,1))
print("Left Knee :", round(features.left_knee_angle,1))
print("Right Knee :", round(features.right_knee_angle,1))
print()
print("POSE FEATURE TEST PASS")
