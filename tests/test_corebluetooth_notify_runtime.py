from engine.corebluetooth_backend import (
    CoreBluetoothAvailability,
    CoreBluetoothBackend,
)


class FakePeripheralManager:
    def __init__(self):
        self.notifications = []

    @property
    def state_name(self):
        return "powered_on"

    def notify(self, characteristic_uuid, payload):
        self.notifications.append((characteristic_uuid, bytes(payload)))


def test_corebluetooth_backend_notify_forwards_to_peripheral_manager(monkeypatch):
    monkeypatch.setattr(
        CoreBluetoothBackend,
        "check_availability",
        staticmethod(lambda: CoreBluetoothAvailability(True, True)),
    )

    peripheral = FakePeripheralManager()
    backend = CoreBluetoothBackend(
        peripheral_manager_factory=lambda: peripheral,
    )

    backend.notify(
        "00002ad1-0000-1000-8000-00805f9b34fb",
        b"\x01\x02\x03",
    )

    assert backend.notifications == [
        ("00002ad1-0000-1000-8000-00805f9b34fb", b"\x01\x02\x03")
    ]
    assert peripheral.notifications == [
        ("00002ad1-0000-1000-8000-00805f9b34fb", b"\x01\x02\x03")
    ]


class FakeMutableCharacteristic:
    def __init__(self, uuid):
        self._uuid = uuid

    def UUID(self):
        return self._uuid


class FakeCBPeripheralManager:
    def __init__(self):
        self.updated_values = []

    def updateValue_forCharacteristic_onSubscribedCentrals_(self, payload, characteristic, centrals):
        self.updated_values.append((bytes(payload), characteristic, centrals))
        return True


def test_corebluetooth_adapter_notify_calls_update_value_for_registered_characteristic():
    from engine.corebluetooth_backend import CoreBluetoothPeripheralManagerAdapter

    adapter = object.__new__(CoreBluetoothPeripheralManagerAdapter)
    adapter._manager = FakeCBPeripheralManager()
    adapter.mutable_characteristics_by_uuid = {
        "00002ad1-0000-1000-8000-00805f9b34fb": FakeMutableCharacteristic("2AD1")
    }
    adapter.notification_results = []

    adapter.notify("00002AD1-0000-1000-8000-00805F9B34FB", b"\x01\x02")

    assert adapter._manager.updated_values == [
        (
            b"\x01\x02",
            adapter.mutable_characteristics_by_uuid["00002ad1-0000-1000-8000-00805f9b34fb"],
            None,
        )
    ]
    assert adapter.notification_results == [True]
