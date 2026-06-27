import math
from engine.profile_manager import ProfileManager


class PhaseClassifier:

    FEATURES = [
        "wrist_to_hip",
        "back_angle",
        "left_elbow",
        "right_elbow",
        "left_knee",
        "right_knee",
    ]

    def __init__(self):
        self.pm = ProfileManager()
        self.profile = self.pm.load()

    def classify(self, features):

        current = {
            "wrist_to_hip": features.wrist_to_hip,
            "back_angle": features.back_angle,
            "left_elbow": features.left_elbow_angle,
            "right_elbow": features.right_elbow_angle,
            "left_knee": features.left_knee_angle,
            "right_knee": features.right_knee_angle,
        }

        best_phase = "UNKNOWN"
        best_score = 1e9

        for phase, target in self.profile.items():

            score = 0

            for key in self.FEATURES:

                score += (current[key] - target[key]) ** 2

            score = math.sqrt(score)

            if score < best_score:
                best_score = score
                best_phase = phase

        return best_phase, best_score
