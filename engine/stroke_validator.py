class StrokeValidator:
    def __init__(self):
        self.min_rom = 8.0
        self.min_drive_speed = 1.5

    def validate(self, data):
        rom = float(data.get("rom", 0.0))
        drive_speed = float(data.get("drive_speed", 0.0))
        phase = data.get("phase", "UNKNOWN")

        valid_phase = phase in ("DRIVE", "FINISH", "RECOVERY", "CATCH")
        valid_rom = rom >= self.min_rom
        valid_speed = drive_speed >= self.min_drive_speed

        valid = valid_phase and valid_rom and valid_speed

        reason = "OK"
        if not valid_phase:
            reason = "BAD_PHASE"
        elif not valid_rom:
            reason = "LOW_ROM"
        elif not valid_speed:
            reason = "LOW_SPEED"

        return {
            "valid": valid,
            "reason": reason,
            "rom": rom,
            "drive_speed": drive_speed,
        }
