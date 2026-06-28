from __future__ import annotations

from dataclasses import dataclass
import importlib
import importlib.util
import time
from typing import Any, Callable

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


class CoreBluetoothPeripheralManagerAdapter:
    def __init__(self) -> None:
        self._manager: Any | None = None
        self._delegate: Any | None = None
        self._state_name = "unknown"
        self._start()

    @property
    def manager(self) -> Any | None:
        return self._manager

    @property
    def state_name(self) -> str:
        return self._state_name


    def pump_run_loop(self, duration_seconds: float = 0.25) -> None:
        if duration_seconds <= 0:
            return

        foundation = importlib.import_module("Foundation")
        run_loop = foundation.NSRunLoop.currentRunLoop()
        deadline = time.monotonic() + duration_seconds

        while time.monotonic() < deadline:
            run_loop.runUntilDate_(
                foundation.NSDate.dateWithTimeIntervalSinceNow_(0.01)
            )

    def _start(self) -> None:
        foundation = importlib.import_module("Foundation")
        corebluetooth = importlib.import_module("CoreBluetooth")

        NSObject = foundation.NSObject
        CBPeripheralManager = corebluetooth.CBPeripheralManager

        adapter = self

        class PeripheralDelegate(NSObject):  # type: ignore[misc, valid-type]
            def peripheralManagerDidUpdateState_(self, peripheral_manager: Any) -> None:
                adapter._state_name = str(getattr(peripheral_manager, "state", lambda: "unknown")())

        self._delegate = PeripheralDelegate.alloc().init()
        self._manager = CBPeripheralManager.alloc().initWithDelegate_queue_options_(
            self._delegate,
            None,
            None,
        )


class CoreBluetoothBackend(BleBackend):
    def __init__(
        self,
        *,
        peripheral_manager_factory: Callable[[], CoreBluetoothPeripheralManagerAdapter] | None = None,
    ) -> None:
        self.availability = self.check_availability()
        self.services: list[BleService] = []
        self.advertisement: BleAdvertisement | None = None
        self.notifications: list[tuple[str, bytes]] = []
        self.peripheral_manager: CoreBluetoothPeripheralManagerAdapter | None = None
        self.peripheral_manager_error: str | None = None

        if not self.availability.ready:
            raise RuntimeError(self.availability.reason())

        factory = peripheral_manager_factory or CoreBluetoothPeripheralManagerAdapter
        try:
            self.peripheral_manager = factory()
        except Exception as exc:
            self.peripheral_manager = None
            self.peripheral_manager_error = f"CBPeripheralManager unavailable: {exc}"

    @property
    def has_peripheral_manager(self) -> bool:
        return self.peripheral_manager is not None

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
