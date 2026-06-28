from __future__ import annotations

from typing import Any, Mapping

from engine.ble_backend import BleAdvertisement, BleBackend
from engine.ftms_constants import FTMS_GATT_PROFILE
from engine.ftms_gatt_service import build_ftms_gatt_service
from engine.ftms_notify_pipeline import FtmsRowerNotifyPipeline


class FtmsBlePeripheralController:
    def __init__(self, backend: BleBackend, local_name: str = "ProjectAtlas") -> None:
        if not local_name:
            raise ValueError("FTMS BLE peripheral local_name is required")
        self.backend = backend
        self.local_name = local_name
        self.notify_pipeline = FtmsRowerNotifyPipeline(backend)
        self.started = False

    def start(self) -> None:
        self.backend.add_service(build_ftms_gatt_service())
        self.backend.start_advertising(
            BleAdvertisement(
                local_name=self.local_name,
                service_uuids=(FTMS_GATT_PROFILE.service_uuid,),
            )
        )
        self.started = True

    def stop(self) -> None:
        self.backend.stop_advertising()
        self.started = False

    def notify_rower_data(self, virtual_rower_data: Mapping[str, Any]) -> bytes:
        if not self.started:
            raise RuntimeError("FTMS BLE peripheral must be started before notify")
        return self.notify_pipeline.notify_rower_data(virtual_rower_data)
