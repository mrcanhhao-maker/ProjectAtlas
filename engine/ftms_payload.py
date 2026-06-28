from __future__ import annotations

from typing import Any, Mapping

from engine.ftms_encoder import FtmsRowingMeasurementEncoder
from engine.ftms_mapper import FtmsMapper, FtmsRowerMeasurement


class FtmsPayloadBuilder:
    def __init__(self) -> None:
        self.mapper = FtmsMapper()
        self.encoder = FtmsRowingMeasurementEncoder()

    def build_rowing_measurement(self, virtual_rower_data: Mapping[str, Any]) -> bytes:
        measurement = self.map_rowing_measurement(virtual_rower_data)
        return self.encoder.encode(measurement)

    def map_rowing_measurement(self, virtual_rower_data: Mapping[str, Any]) -> FtmsRowerMeasurement:
        return self.mapper.map_virtual_rower(virtual_rower_data)
