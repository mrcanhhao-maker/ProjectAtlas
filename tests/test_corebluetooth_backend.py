from __future__ import annotations

import pytest

from engine.ble_backend import BleAdvertisement, BleCharacteristic, BleService
from engine.corebluetooth_backend import CoreBluetoothAvailability, CoreBluetoothBackend, CoreBluetoothPeripheralManagerAdapter


class FakePeripheralManager:
    @property
    def state_name(self) -> str:
        return "fake-ready"


def test_corebluetooth_availability_reports_missing_dependencies():
    availability = CoreBluetoothAvailability(
        pyobjc_available=False,
        corebluetooth_available=False,
    )

    assert availability.ready is False
    assert "PyObjC" in availability.reason()
    assert "CoreBluetooth" in availability.reason()


def test_corebluetooth_availability_reports_ready_when_dependencies_exist():
    availability = CoreBluetoothAvailability(
        pyobjc_available=True,
        corebluetooth_available=True,
    )

    assert availability.ready is True
    assert availability.reason() == "CoreBluetooth backend dependencies available"


def test_corebluetooth_backend_refuses_to_start_without_dependencies(monkeypatch):
    monkeypatch.setattr(
        CoreBluetoothBackend,
        "check_availability",
        staticmethod(lambda: CoreBluetoothAvailability(False, False)),
    )

    with pytest.raises(RuntimeError) as error:
        CoreBluetoothBackend()

    assert "PyObjC" in str(error.value)
    assert "CoreBluetooth" in str(error.value)


def test_corebluetooth_backend_implements_ble_backend_contract_when_dependencies_exist(monkeypatch):
    monkeypatch.setattr(
        CoreBluetoothBackend,
        "check_availability",
        staticmethod(lambda: CoreBluetoothAvailability(True, True)),
    )

    backend = CoreBluetoothBackend(peripheral_manager_factory=FakePeripheralManager)
    service = BleService(
        uuid="service",
        characteristics=(
            BleCharacteristic(uuid="char", properties=("notify",)),
        ),
    )
    advertisement = BleAdvertisement(
        local_name="ProjectAtlas",
        service_uuids=("service",),
    )

    backend.add_service(service)
    backend.start_advertising(advertisement)
    backend.notify("char", b"\x01\x02")
    backend.stop_advertising()

    assert backend.services == [service]
    assert backend.advertisement is None
    assert backend.notifications == [("char", b"\x01\x02")]
    assert backend.has_peripheral_manager is True
    assert backend.peripheral_manager_error is None


def test_corebluetooth_backend_keeps_running_when_real_peripheral_manager_is_guarded(monkeypatch):
    monkeypatch.setattr(
        CoreBluetoothBackend,
        "check_availability",
        staticmethod(lambda: CoreBluetoothAvailability(True, True)),
    )

    def broken_factory():
        raise RuntimeError("permission denied")

    backend = CoreBluetoothBackend(peripheral_manager_factory=broken_factory)

    assert backend.has_peripheral_manager is False
    assert backend.peripheral_manager is None
    assert backend.peripheral_manager_error == "CBPeripheralManager unavailable: permission denied"


def test_corebluetooth_backend_peripheral_manager_adapter_can_pump_run_loop(monkeypatch):
    import engine.corebluetooth_backend as module

    events = []

    class FakeDate:
        @staticmethod
        def dateWithTimeIntervalSinceNow_(seconds):
            events.append(("date", seconds))
            return "fake-date"

    class FakeRunLoop:
        def runUntilDate_(self, date):
            events.append(("run", date))

    class FakeNSRunLoop:
        @staticmethod
        def currentRunLoop():
            return FakeRunLoop()

    class FakeFoundation:
        NSDate = FakeDate
        NSRunLoop = FakeNSRunLoop

    monkeypatch.setattr(module.importlib, "import_module", lambda name: FakeFoundation)

    adapter = object.__new__(module.CoreBluetoothPeripheralManagerAdapter)
    adapter.pump_run_loop(0.02)

    assert any(event[0] == "date" for event in events)
    assert any(event[0] == "run" for event in events)


def test_corebluetooth_peripheral_manager_adapter_maps_manager_state_name():
    class Manager:
        def __init__(self, state):
            self._state = state

        def state(self):
            return self._state

    assert CoreBluetoothPeripheralManagerAdapter.read_manager_state_name(Manager(0)) == "unknown"
    assert CoreBluetoothPeripheralManagerAdapter.read_manager_state_name(Manager(5)) == "powered_on"
    assert CoreBluetoothPeripheralManagerAdapter.read_manager_state_name(Manager(99)) == "unknown_99"


def test_corebluetooth_peripheral_manager_adapter_handles_unreadable_manager_state():
    class MissingState:
        pass

    class BrokenState:
        def state(self):
            raise RuntimeError("boom")

    assert CoreBluetoothPeripheralManagerAdapter.read_manager_state_name(MissingState()) == "unknown"
    assert CoreBluetoothPeripheralManagerAdapter.read_manager_state_name(BrokenState()) == "unknown"


def test_corebluetooth_backend_add_service_forwards_to_peripheral_manager(monkeypatch):
    monkeypatch.setattr(
        CoreBluetoothBackend,
        "check_availability",
        staticmethod(lambda: CoreBluetoothAvailability(True, True)),
    )

    class CapturingPeripheralManager:
        def __init__(self):
            self.added_services = []

        @property
        def state_name(self):
            return "powered_on"

        def add_service(self, service):
            self.added_services.append(service)

    peripheral = CapturingPeripheralManager()
    backend = CoreBluetoothBackend(peripheral_manager_factory=lambda: peripheral)
    service = BleService(
        uuid="service",
        characteristics=(BleCharacteristic(uuid="char", properties=("read", "notify")),),
    )

    backend.add_service(service)

    assert backend.services == [service]
    assert peripheral.added_services == [service]


def test_corebluetooth_peripheral_manager_adapter_maps_properties_and_permissions(monkeypatch):
    import engine.corebluetooth_backend as module

    class FakeCoreBluetooth:
        CBCharacteristicPropertyRead = 2
        CBCharacteristicPropertyWriteWithoutResponse = 4
        CBCharacteristicPropertyWrite = 8
        CBCharacteristicPropertyNotify = 16
        CBAttributePermissionsReadable = 1
        CBAttributePermissionsWriteable = 2

    monkeypatch.setattr(module.importlib, "import_module", lambda name: FakeCoreBluetooth)

    properties = CoreBluetoothPeripheralManagerAdapter._map_characteristic_properties(
        ("read", "notify", "write", "write_without_response")
    )
    permissions = CoreBluetoothPeripheralManagerAdapter._map_characteristic_permissions(
        ("read", "write", "write_without_response")
    )

    assert properties == 30
    assert permissions == 3


def test_corebluetooth_peripheral_manager_adapter_tracks_service_add_result():
    adapter = object.__new__(CoreBluetoothPeripheralManagerAdapter)
    adapter.added_service_count = 0
    adapter.service_errors = []

    adapter.added_service_count += 1
    adapter.service_errors.append("boom")

    assert adapter.added_service_count == 1
    assert adapter.service_errors == ["boom"]
