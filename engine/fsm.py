from collections import deque


class StrokeFSM:
    VALID_TRANSITIONS = {
        "READY": ["RECOVERY", "CATCH"],
        "RECOVERY": ["CATCH"],
        "CATCH": ["DRIVE"],
        "DRIVE": ["FINISH"],
        "FINISH": ["RECOVERY"],
    }

    def __init__(self, confirm_frames=3):
        self.state = "READY"
        self.last_state = "READY"
        self.confirm_frames = confirm_frames
        self.buffer = deque(maxlen=confirm_frames)
        self.completed_stroke = False
        self.state_changed = False

    def update(self, candidate):
        self.completed_stroke = False
        self.state_changed = False

        if candidate == "UNKNOWN":
            return self.state

        self.buffer.append(candidate)

        if len(self.buffer) < self.confirm_frames:
            return self.state

        if len(set(self.buffer)) != 1:
            return self.state

        confirmed = self.buffer[-1]

        if confirmed == self.state:
            return self.state

        allowed = self.VALID_TRANSITIONS.get(self.state, [])

        if confirmed in allowed:
            old = self.state
            self.last_state = old
            self.state = confirmed
            self.state_changed = True

            if old == "FINISH" and confirmed == "RECOVERY":
                self.completed_stroke = True

        return self.state
