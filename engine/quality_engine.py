class QualityEngine:
    def __init__(self):
        self.score = 0

    def update(self, data):
        confidence = data.get("confidence", 0.0)

        if confidence >= 0.95:
            score = 100
        elif confidence >= 0.90:
            score = 90
        elif confidence >= 0.80:
            score = 80
        elif confidence >= 0.70:
            score = 70
        else:
            score = int(confidence * 100)

        return {"quality": score}
