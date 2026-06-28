from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class FtmsRowerMeasurement:
    elapsed_time_s: float
    stroke_rate_spm: float
    stroke_count: int
    distance_m: float
    speed_mps: float
    pace_500m_s: float
    power_watts: int
    moving: bool


class FtmsMapper:
    def map_virtual_rower(self, data: Mapping[str, Any]) -> FtmsRowerMeasurement:
        elapsed = self._float(data.get("elapsed_time_s", data.get("elapsed", 0.0)))
        spm = self._float(data.get("spm", data.get("stroke_rate_spm", 0.0)))
        strokes = self._int(data.get("stroke_count", 0))
        distance = self._float(data.get("distance_m", 0.0))
        speed = self._float(data.get("speed_mps", data.get("speed", 0.0)))
        pace = self._float(data.get("pace_500m_s", data.get("pace_500m", 0.0)))
        watts = self._int(data.get("watts", data.get("power_watts", data.get("virtual_watts", 0))))
        moving = bool(data.get("moving", speed > 0.01 or watts > 0))

        return FtmsRowerMeasurement(
            elapsed_time_s=max(0.0, elapsed),
            stroke_rate_spm=max(0.0, spm),
            stroke_count=max(0, strokes),
            distance_m=max(0.0, distance),
            speed_mps=max(0.0, speed),
            pace_500m_s=max(0.0, pace),
            power_watts=max(0, watts),
            moving=moving,
        )

    @staticmethod
    def _float(value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _int(value: Any) -> int:
        try:
            return int(round(float(value)))
        except (TypeError, ValueError):
            return 0
