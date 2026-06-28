from __future__ import annotations

from dataclasses import dataclass
import importlib
import importlib.util
import time
from typing import Any, Callable

from engine.ble_backend import BleAdvertisement, BleBackend, BleCharacteristic, BleService


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
    STATE_NAMES = {
        0: "unknown",
        1: "resetting",
        2: "unsupported",
        3: "unauthorized",
        4: "powered_off",
        5: "powered_on",
    }

    def __init__(self) -> None:
        self._manager: Any | None = None
        self._delegate: Any | None = None
        self._state_name = "unknown"
        self.added_service_count = 0
        self.service_errors: list[str] = []
        self._start()

    @property
    def manager(self) -> Any | None:
        return self._manager

    @property
    def state_name(self) -> str:
        if self._manager is not None:
            self._state_name = self.read_manager_state_name(self._manager)
        return self._state_name

    @classmethod
    def read_manager_state_name(cls, manager: Any) -> str:
        state_selector = getattr(manager, "state", None)
        if not callable(state_selector):
            return "unknown"

        try:
            raw_state = int(state_selector())
        except Exception:
            return "unknown"

        return cls.STATE_NAMES.get(raw_state, f"unknown_{raw_state}")


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

    def build_mutable_service(self, service: BleService) -> Any:
        corebluetooth = importlib.import_module("CoreBluetooth")
        cb_service = corebluetooth.CBMutableService.alloc().initWithType_primary_(
            self._build_uuid(service.uuid),
            True,
        )
        cb_service.setCharacteristics_(
            [self.build_mutable_characteristic(characteristic) for characteristic in service.characteristics]
        )
        return cb_service

    def build_mutable_characteristic(self, characteristic: BleCharacteristic) -> Any:
        corebluetooth = importlib.import_module("CoreBluetooth")
        return corebluetooth.CBMutableCharacteristic.alloc().initWithType_properties_value_permissions_(
            self._build_uuid(characteristic.uuid),
            self._map_characteristic_properties(characteristic.properties),
            None,
            self._map_characteristic_permissions(characteristic.properties),
        )

    def add_service(self, service: BleService) -> Any:
        if self._manager is None:
            raise RuntimeError("CBPeripheralManager is not initialized")
        cb_service = self.build_mutable_service(service)
        self._manager.addService_(cb_service)
        return cb_service

    @staticmethod
    def _build_uuid(uuid: str) -> Any:
        corebluetooth = importlib.import_module("CoreBluetooth")
        return corebluetooth.CBUUID.UUIDWithString_(uuid)

    @staticmethod
    def _map_characteristic_properties(properties: tuple[str, ...]) -> int:
        corebluetooth = importlib.import_module("CoreBluetooth")
        value = 0
        if "read" in properties:
            value |= int(corebluetooth.CBCharacteristicPropertyRead)
        if "notify" in properties:
            value |= int(corebluetooth.CBCharacteristicPropertyNotify)
        if "write" in properties:
            value |= int(corebluetooth.CBCharacteristicPropertyWrite)
        if "write_without_response" in properties:
            value |= int(corebluetooth.CBCharacteristicPropertyWriteWithoutResponse)
        return value

    @staticmethod
    def _map_characteristic_permissions(properties: tuple[str, ...]) -> int:
        corebluetooth = importlib.import_module("CoreBluetooth")
        value = 0
        if "read" in properties:
            value |= int(corebluetooth.CBAttributePermissionsReadable)
        if "write" in properties or "write_without_response" in properties:
            value |= int(corebluetooth.CBAttributePermissionsWriteable)
        return value

    def _start(self) -> None:
        foundation = importlib.import_module("Foundation")
        corebluetooth = importlib.import_module("CoreBluetooth")

        NSObject = foundation.NSObject
        CBPeripheralManager = corebluetooth.CBPeripheralManager

        adapter = self

        class PeripheralDelegate(NSObject):  # type: ignore[misc, valid-type]
            def peripheralManagerDidUpdateState_(self, peripheral_manager: Any) -> None:
                adapter._state_name = adapter.read_manager_state_name(peripheral_manager)

            def peripheralManager_didAddService_error_(self, peripheral_manager: Any, service: Any, error: Any) -> None:
                if error is None:
                    adapter.added_service_count += 1
                    return
                adapter.service_errors.append(str(error))

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
        add_service = getattr(self.peripheral_manager, "add_service", None)
        if callable(add_service):
            add_service(service)

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
