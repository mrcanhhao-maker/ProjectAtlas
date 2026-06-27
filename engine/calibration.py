import json
import os


class CalibrationEngine:

    def __init__(self):
        self.samples = {
            "RECOVERY": [],
            "CATCH": [],
            "DRIVE": [],
            "FINISH": [],
        }

    def add_sample(self, phase, features):

        self.samples[phase].append(
            {
                "wrist_to_hip": features.wrist_to_hip,
                "back_angle": features.back_angle,
                "left_elbow": features.left_elbow_angle,
                "right_elbow": features.right_elbow_angle,
                "left_knee": features.left_knee_angle,
                "right_knee": features.right_knee_angle,
            }
        )

    def _average(self, data, key):
        if len(data) == 0:
            return 0

        return sum(x[key] for x in data) / len(data)

    def build_profile(self):

        profile = {}

        for phase in self.samples:

            s = self.samples[phase]

            profile[phase] = {
                "wrist_to_hip": self._average(s, "wrist_to_hip"),
                "back_angle": self._average(s, "back_angle"),
                "left_elbow": self._average(s, "left_elbow"),
                "right_elbow": self._average(s, "right_elbow"),
                "left_knee": self._average(s, "left_knee"),
                "right_knee": self._average(s, "right_knee"),
            }

        return profile

    def save(self, filename="profiles/default.json"):

        profile = self.build_profile()

        os.makedirs("profiles", exist_ok=True)

        with open(filename, "w") as f:
            json.dump(profile, f, indent=4)

        return filename
