import json
import os


class ProfileManager:

    def __init__(self, filename="profiles/default.json"):
        self.filename = filename
        self.profile = None

    def load(self):
        if not os.path.exists(self.filename):
            raise FileNotFoundError(self.filename)

        with open(self.filename, "r") as f:
            self.profile = json.load(f)

        return self.profile

    def get(self, phase):
        if self.profile is None:
            self.load()

        return self.profile.get(phase, {})
