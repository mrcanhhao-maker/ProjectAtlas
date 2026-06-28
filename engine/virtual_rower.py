from __future__ import annotations

import math
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class VirtualRowerState:
    timestamp: float
    stroke_count: int
    stroke_rate_spm: float
    power_watts: int
    pace_500m: float
    speed_mps: float
    distance_m: float
    drive_ratio: float
    quality_score: float
    is_moving: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class VirtualRowerEngine:
    """
    Production core for Stage 2.

    Converts camera rowing motion signals into a stable virtual rowing machine state.
    This engine does not handle BLE, FTMS, Bluetooth advertising, or MyWhoosh directly.
    """

    def __init__(
        self,
        drag_factor: float = 115.0,
        min_power_watts: int = 0,
        max_power_watts: int = 650,
        idle_timeout_s: float = 2.5,
    ) -> None:
        self.drag_factor = float(drag_factor)
        self.min_power_watts = int(min_power_watts)
        self.max_power_watts = int(max_power_watts)
        self.idle_timeout_s = float(idle_timeout_s)

        self._distance_m = 0.0
        self._last_timestamp: Optional[float] = None
        self._last_moving_timestamp: Optional[float] = None
        self._last_stroke_count = 0
        self._last_state = VirtualRowerState(
            timestamp=time.time(),
            stroke_count=0,
            stroke_rate_spm=0.0,
            power_watts=0,
            pace_500m=0.0,
            speed_mps=0.0,
            distance_m=0.0,
            drive_ratio=0.0,
            quality_score=0.0,
            is_moving=False,
        )

    def reset(self) -> VirtualRowerState:
        self._distance_m = 0.0
        self._last_timestamp = None
        self._last_moving_timestamp = None
        self._last_stroke_count = 0
        self._last_state = VirtualRowerState(
            timestamp=time.time(),
            stroke_count=0,
            stroke_rate_spm=0.0,
            power_watts=0,
            pace_500m=0.0,
            speed_mps=0.0,
            distance_m=0.0,
            drive_ratio=0.0,
            quality_score=0.0,
            is_moving=False,
        )
        return self._last_state

    def update(self, stroke_data: Dict[str, Any], timestamp: Optional[float] = None) -> Dict[str, Any]:
        now = float(timestamp if timestamp is not None else time.time())

        dt = 0.0
        if self._last_timestamp is not None:
            dt = max(0.0, now - self._last_timestamp)
        self._last_timestamp = now

        stroke_count = self._read_int(stroke_data, "stroke_count", self._last_stroke_count)
        spm = self._read_float(stroke_data, "spm", 0.0)
        quality_score = self._read_float(stroke_data, "quality_score", self._read_float(stroke_data, "confidence", 0.0))
        drive_ratio = self._read_float(stroke_data, "drive_ratio", 0.0)

        stroke_delta = max(0, stroke_count - self._last_stroke_count)
        self._last_stroke_count = stroke_count

        is_active_signal = spm >= 8.0 or stroke_delta > 0
        if is_active_signal:
            self._last_moving_timestamp = now

        is_moving = (
            self._last_moving_timestamp is not None
            and (now - self._last_moving_timestamp) <= self.idle_timeout_s
        )

        power = self._estimate_power_watts(
            spm=spm,
            quality_score=quality_score,
            drive_ratio=drive_ratio,
            stroke_delta=stroke_delta,
            is_moving=is_moving,
        )

        speed = self._power_to_speed_mps(power)
        if is_moving and dt > 0:
            self._distance_m += speed * dt

        pace = self._speed_to_pace_500m(speed)

        self._last_state = VirtualRowerState(
            timestamp=now,
            stroke_count=stroke_count,
            stroke_rate_spm=round(spm, 1),
            power_watts=power,
            pace_500m=round(pace, 1),
            speed_mps=round(speed, 3),
            distance_m=round(self._distance_m, 2),
            drive_ratio=round(drive_ratio, 3),
            quality_score=round(quality_score, 3),
            is_moving=is_moving,
        )
        return self._last_state.to_dict()

    def state(self) -> Dict[str, Any]:
        return self._last_state.to_dict()

    def _estimate_power_watts(
        self,
        spm: float,
        quality_score: float,
        drive_ratio: float,
        stroke_delta: int,
        is_moving: bool,
    ) -> int:
        if not is_moving:
            return 0

        normalized_spm = max(0.0, min(spm, 42.0)) / 30.0
        normalized_quality = max(0.15, min(quality_score, 1.0))
        normalized_drive = max(0.35, min(drive_ratio if drive_ratio > 0 else 0.8, 1.4))

        base_power = 95.0 * (normalized_spm ** 2.7)
        drag_multiplier = max(0.75, min(self.drag_factor / 115.0, 1.35))
        stroke_boost = 1.08 if stroke_delta > 0 else 1.0

        watts = base_power * normalized_quality * normalized_drive * drag_multiplier * stroke_boost
        return int(max(self.min_power_watts, min(round(watts), self.max_power_watts)))

    @staticmethod
    def _power_to_speed_mps(power_watts: int) -> float:
        if power_watts <= 0:
            return 0.0
        pace_seconds = ((2.80 / float(power_watts)) ** (1.0 / 3.0)) * 500.0
        if pace_seconds <= 0:
            return 0.0
        return 500.0 / pace_seconds

    @staticmethod
    def _speed_to_pace_500m(speed_mps: float) -> float:
        if speed_mps <= 0:
            return 0.0
        return 500.0 / speed_mps

    @staticmethod
    def _read_float(data: Dict[str, Any], key: str, default: float) -> float:
        try:
            value = data.get(key, default)
            if value is None or isinstance(value, bool):
                return float(default)
            value = float(value)
            if math.isnan(value) or math.isinf(value):
                return float(default)
            return value
        except (TypeError, ValueError):
            return float(default)

    @staticmethod
    def _read_int(data: Dict[str, Any], key: str, default: int) -> int:
        try:
            value = data.get(key, default)
            if value is None or isinstance(value, bool):
                return int(default)
            return int(value)
        except (TypeError, ValueError):
            return int(default)
