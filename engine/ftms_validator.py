from __future__ import annotations

from dataclasses import dataclass
from typing import List

from engine.ftms_decoder import FtmsRowingMeasurementDecoder


@dataclass(frozen=True)
class FtmsValidationResult:
    ok: bool
    errors: List[str]


class FtmsPayloadValidator:
    def __init__(self) -> None:
        self.decoder = FtmsRowingMeasurementDecoder()

    def validate_rowing_measurement(self, payload: bytes) -> FtmsValidationResult:
        errors: List[str] = []

        if not isinstance(payload, (bytes, bytearray)):
            return FtmsValidationResult(False, ["payload must be bytes"])

        if len(payload) != 14:
            errors.append(f"payload length must be 14 bytes, got {len(payload)}")

        try:
            decoded = self.decoder.decode(bytes(payload))
        except ValueError as exc:
            errors.append(str(exc))
            return FtmsValidationResult(False, errors)

        if decoded["stroke_rate_spm"] < 0:
            errors.append("stroke_rate_spm must be non-negative")

        if decoded["stroke_count"] < 0:
            errors.append("stroke_count must be non-negative")

        if decoded["distance_m"] < 0:
            errors.append("distance_m must be non-negative")

        if decoded["pace_500m_s"] < 0:
            errors.append("pace_500m_s must be non-negative")

        if decoded["elapsed_time_s"] < 0:
            errors.append("elapsed_time_s must be non-negative")

        return FtmsValidationResult(len(errors) == 0, errors)
