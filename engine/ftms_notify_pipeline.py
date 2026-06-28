from __future__ import annotations

from typing import Any, Mapping

from engine.ble_backend import BleBackend
from engine.ftms_constants import FTMS_GATT_PROFILE
from engine.ftms_payload import FtmsPayloadBuilder
from engine.ftms_validator import FtmsPayloadValidator


class FtmsRowerNotifyPipeline:
    def __init__(self, backend: BleBackend) -> None:
        self.backend = backend
        self.payload_builder = FtmsPayloadBuilder()
        self.validator = FtmsPayloadValidator()

    def notify_rower_data(self, virtual_rower_data: Mapping[str, Any]) -> bytes:
        payload = self.payload_builder.build_rowing_measurement(virtual_rower_data)
        validation = self.validator.validate_rowing_measurement(payload)

        if not validation.ok:
            raise ValueError(f"Invalid FTMS rower payload: {validation.errors}")

        self.backend.notify(FTMS_GATT_PROFILE.rower_data_uuid, payload)
        return payload
