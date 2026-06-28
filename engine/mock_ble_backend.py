from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from engine.ble_backend import BleAdvertisement, BleService, service_characteristic_map


@dataclass
class BleNotification:
    characteristic_uuid: str
    payload: bytes


@dataclass
class MockBleBackend:
    services: List[BleService] = field(default_factory=list)
    advertisement: Optional[BleAdvertisement] = None
    notifications: List[BleNotification] = field(default_factory=list)

    def add_service(self, service: BleService) -> None:
        if any(existing.uuid == service.uuid for existing in self.services):
            raise ValueError(f"BLE service already exists: {service.uuid}")
        self.services.append(service)

    def start_advertising(self, advertisement: BleAdvertisement) -> None:
        if not advertisement.local_name:
            raise ValueError("BLE advertisement local_name is required")
        if not advertisement.service_uuids:
            raise ValueError("BLE advertisement requires at least one service UUID")
        self.advertisement = advertisement

    def stop_advertising(self) -> None:
        self.advertisement = None

    def notify(self, characteristic_uuid: str, payload: bytes) -> None:
        if not isinstance(payload, (bytes, bytearray)):
            raise TypeError("BLE notify payload must be bytes")

        known_characteristics = {}
        for service in self.services:
            known_characteristics.update(service_characteristic_map(service))

        characteristic = known_characteristics.get(characteristic_uuid)
        if characteristic is None:
            raise ValueError(f"Unknown BLE characteristic: {characteristic_uuid}")

        if "notify" not in characteristic.properties:
            raise ValueError(f"BLE characteristic is not notifiable: {characteristic_uuid}")

        self.notifications.append(
            BleNotification(
                characteristic_uuid=characteristic_uuid,
                payload=bytes(payload),
            )
        )
