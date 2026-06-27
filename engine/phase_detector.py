class PhaseDetector:
    def detect(self, features):
        if not features.body_found or features.confidence < 0.35:
            return "UNKNOWN"

        elbow = (features.left_elbow_angle + features.right_elbow_angle) / 2
        knee = (features.left_knee_angle + features.right_knee_angle) / 2
        wrist = features.wrist_to_hip
        back = features.back_angle

        if wrist > 0.12 and knee < 130:
            return "CATCH"

        if wrist < -0.08 and elbow < 120:
            return "FINISH"

        if wrist < 0.08 and knee > 135:
            return "DRIVE"

        if wrist > 0.02 and elbow > 130:
            return "RECOVERY"

        return "UNKNOWN"
