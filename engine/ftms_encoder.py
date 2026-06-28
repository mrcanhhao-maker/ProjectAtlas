from __future__ import annotations

import struct

from engine.ftms_mapper import FtmsRowerMeasurement


class FtmsRowingMeasurementEncoder:
    FLAG_MORE_DATA = 1 << 0
    FLAG_AVERAGE_STROKE_RATE_PRESENT = 1 << 1
    FLAG_TOTAL_DISTANCE_PRESENT = 1 << 2
    FLAG_INSTANTANEOUS_PACE_PRESENT = 1 << 3
    FLAG_AVERAGE_PACE_PRESENT = 1 << 4
    FLAG_INSTANTANEOUS_POWER_PRESENT = 1 << 5
    FLAG_AVERAGE_POWER_PRESENT = 1 << 6
    FLAG_RESISTANCE_LEVEL_PRESENT = 1 << 7
    FLAG_EXPENDED_ENERGY_PRESENT = 1 << 8
    FLAG_HEART_RATE_PRESENT = 1 << 9
    FLAG_METABOLIC_EQUIVALENT_PRESENT = 1 << 10
    FLAG_ELAPSED_TIME_PRESENT = 1 << 11
    FLAG_REMAINING_TIME_PRESENT = 1 << 12

    def encode(self, measurement: FtmsRowerMeasurement) -> bytes:
        flags = (
            self.FLAG_TOTAL_DISTANCE_PRESENT
            | self.FLAG_INSTANTANEOUS_PACE_PRESENT
            | self.FLAG_INSTANTANEOUS_POWER_PRESENT
            | self.FLAG_ELAPSED_TIME_PRESENT
        )

        stroke_rate_half_spm = self._u8(round(measurement.stroke_rate_spm * 2.0))
        stroke_count = self._u16(measurement.stroke_count)
        distance = self._u24(round(measurement.distance_m))
        pace = self._u16(round(measurement.pace_500m_s))
        power = self._s16(measurement.power_watts)
        elapsed = self._u16(round(measurement.elapsed_time_s))

        payload = bytearray()
        payload.extend(struct.pack("<H", flags))
        payload.extend(struct.pack("<BH", stroke_rate_half_spm, stroke_count))
        payload.extend(distance)
        payload.extend(struct.pack("<H", pace))
        payload.extend(struct.pack("<h", power))
        payload.extend(struct.pack("<H", elapsed))

        return bytes(payload)

    @staticmethod
    def _u8(value: int) -> int:
        return max(0, min(255, int(value)))

    @staticmethod
    def _u16(value: int) -> int:
        return max(0, min(65535, int(value)))

    @staticmethod
    def _s16(value: int) -> int:
        return max(-32768, min(32767, int(value)))

    @staticmethod
    def _u24(value: int) -> bytes:
        value = max(0, min(16777215, int(value)))
        return bytes((value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF))
