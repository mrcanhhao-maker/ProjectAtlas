from __future__ import annotations

import pytest

from engine.ble_backend import BleAdvertisement, BleCharacteristic, BleService
from engine.corebluetooth_backend import CoreBluetoothAvailability, CoreBluetoothBackend


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

    backend = CoreBluetoothBackend()
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
