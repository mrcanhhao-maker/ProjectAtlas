from dataclasses import dataclass
from engine.geometry import angle, distance, midpoint


@dataclass
class PoseFeatures:
    body_found: bool = False

    wrist_y: float = 0.0
    hip_y: float = 0.0
    knee_y: float = 0.0

    wrist_to_hip: float = 0.0
    shoulder_width: float = 0.0

    left_elbow_angle: float = 0.0
    right_elbow_angle: float = 0.0
    left_knee_angle: float = 0.0
    right_knee_angle: float = 0.0
    back_angle: float = 0.0

    confidence: float = 0.0


class PoseFeatureExtractor:
    def extract(self, landmarks):
        if landmarks is None:
            return PoseFeatures(body_found=False)

        try:
            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]
            left_elbow = landmarks[13]
            right_elbow = landmarks[14]
            left_wrist = landmarks[15]
            right_wrist = landmarks[16]
            left_hip = landmarks[23]
            right_hip = landmarks[24]
            left_knee = landmarks[25]
            right_knee = landmarks[26]
            left_ankle = landmarks[27]
            right_ankle = landmarks[28]
        except Exception:
            return PoseFeatures(body_found=False)

        wrist_y = (left_wrist.y + right_wrist.y) / 2
        hip_y = (left_hip.y + right_hip.y) / 2
        knee_y = (left_knee.y + right_knee.y) / 2

        shoulder_width = distance(left_shoulder, right_shoulder)

        left_elbow_angle = angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = angle(right_shoulder, right_elbow, right_wrist)

        left_knee_angle = angle(left_hip, left_knee, left_ankle)
        right_knee_angle = angle(right_hip, right_knee, right_ankle)

        # Góc thân người tạm tính: shoulder - hip - knee
        back_angle = angle(left_shoulder, left_hip, left_knee)

        visible_points = [
            left_shoulder, right_shoulder,
            left_elbow, right_elbow,
            left_wrist, right_wrist,
            left_hip, right_hip,
            left_knee, right_knee,
            left_ankle, right_ankle,
        ]

        confidence = sum(p.visibility for p in visible_points) / len(visible_points)

        return PoseFeatures(
            body_found=True,
            wrist_y=wrist_y,
            hip_y=hip_y,
            knee_y=knee_y,
            wrist_to_hip=wrist_y - hip_y,
            shoulder_width=shoulder_width,
            left_elbow_angle=left_elbow_angle,
            right_elbow_angle=right_elbow_angle,
            left_knee_angle=left_knee_angle,
            right_knee_angle=right_knee_angle,
            back_angle=back_angle,
            confidence=confidence,
        )
