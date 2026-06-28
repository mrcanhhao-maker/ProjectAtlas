from engine.ble_backend import BleAdvertisement, BleCharacteristic, BleService
from engine.mock_ble_backend import MockBleBackend


def test_mock_ble_backend_adds_service_and_advertises():
    backend = MockBleBackend()
    service = BleService(
        uuid="service",
        characteristics=(BleCharacteristic(uuid="char", properties=("notify",)),),
    )
    advertisement = BleAdvertisement(local_name="ProjectAtlas", service_uuids=("service",))

    backend.add_service(service)
    backend.start_advertising(advertisement)

    assert backend.services == [service]
    assert backend.advertisement is advertisement


def test_mock_ble_backend_notifies_known_notify_characteristic():
    backend = MockBleBackend()
    backend.add_service(
        BleService(
            uuid="service",
            characteristics=(BleCharacteristic(uuid="char", properties=("notify",)),),
        )
    )

    backend.notify("char", b"\x01\x02")

    assert len(backend.notifications) == 1
    assert backend.notifications[0].characteristic_uuid == "char"
    assert backend.notifications[0].payload == b"\x01\x02"


def test_mock_ble_backend_rejects_duplicate_service():
    backend = MockBleBackend()
    service = BleService(uuid="service", characteristics=())

    backend.add_service(service)

    try:
        backend.add_service(service)
    except ValueError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("Expected duplicate service rejection")


def test_mock_ble_backend_rejects_unknown_characteristic_notify():
    backend = MockBleBackend()

    try:
        backend.notify("missing", b"\x00")
    except ValueError as exc:
        assert "Unknown BLE characteristic" in str(exc)
    else:
        raise AssertionError("Expected unknown characteristic rejection")
