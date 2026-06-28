from __future__ import annotations

from dataclasses import dataclass
import importlib.util

from engine.ble_backend import BleAdvertisement, BleBackend, BleService


@dataclass(frozen=True)
class CoreBluetoothAvailability:
    pyobjc_available: bool
    corebluetooth_available: bool

    @property
    def ready(self) -> bool:
        return self.pyobjc_available and self.corebluetooth_available

    def reason(self) -> str:
        missing = []
        if not self.pyobjc_available:
            missing.append("PyObjC")
        if not self.corebluetooth_available:
            missing.append("CoreBluetooth")
        if missing:
            return "CoreBluetooth backend unavailable; missing: " + ", ".join(missing)
        return "CoreBluetooth backend dependencies available"


class CoreBluetoothBackend(BleBackend):
    def __init__(self) -> None:
        self.availability = self.check_availability()
        self.services: list[BleService] = []
        self.advertisement: BleAdvertisement | None = None
        self.notifications: list[tuple[str, bytes]] = []

        if not self.availability.ready:
            raise RuntimeError(self.availability.reason())

    def add_service(self, service: BleService) -> None:
        self.services.append(service)

    def start_advertising(self, advertisement: BleAdvertisement) -> None:
        self.advertisement = advertisement

    def stop_advertising(self) -> None:
        self.advertisement = None

    def notify(self, characteristic_uuid: str, payload: bytes) -> None:
        self.notifications.append((characteristic_uuid, bytes(payload)))

    @staticmethod
    def check_availability() -> CoreBluetoothAvailability:
        return CoreBluetoothAvailability(
            pyobjc_available=importlib.util.find_spec("objc") is not None,
            corebluetooth_available=importlib.util.find_spec("CoreBluetooth") is not None,
        )
