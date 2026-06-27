import time
from engine.calibration import CalibrationEngine


class CalibrationWizard:

    PHASES = [
        ("RECOVERY", 3),
        ("CATCH", 3),
        ("DRIVE", 3),
        ("FINISH", 3),
    ]

    def __init__(self):
        self.engine = CalibrationEngine()

    def run(self, feature_provider):

        print()
        print("========== AUTO CALIBRATION ==========")

        for phase, seconds in self.PHASES:

            print()
            print(f"Move to {phase}")

            for i in range(3, 0, -1):
                print(i)
                time.sleep(1)

            print("Recording...")

            start = time.time()

            while time.time() - start < seconds:

                feature = feature_provider()

                if feature.body_found:
                    self.engine.add_sample(phase, feature)

                time.sleep(0.03)

            print(f"{phase} OK")

        filename = self.engine.save()

        print()
        print("Calibration Complete")
        print(filename)

        return filename
