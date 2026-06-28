from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol


@dataclass(frozen=True)
class BleCharacteristic:
    uuid: str
    properties: tuple[str, ...]


@dataclass(frozen=True)
class BleService:
    uuid: str
    characteristics: tuple[BleCharacteristic, ...]


@dataclass(frozen=True)
class BleAdvertisement:
    local_name: str
    service_uuids: tuple[str, ...]


class BleBackend(Protocol):
    def add_service(self, service: BleService) -> None:
        ...

    def start_advertising(self, advertisement: BleAdvertisement) -> None:
        ...

    def stop_advertising(self) -> None:
        ...

    def notify(self, characteristic_uuid: str, payload: bytes) -> None:
        ...


def service_characteristic_map(service: BleService) -> Dict[str, BleCharacteristic]:
    return {characteristic.uuid: characteristic for characteristic in service.characteristics}
