from engine.ftms_ble_peripheral import FtmsBlePeripheralController
from engine.ftms_constants import FTMS_GATT_PROFILE
from engine.mock_ble_backend import MockBleBackend


def test_ftms_ble_peripheral_start_registers_service_and_advertising():
    backend = MockBleBackend()
    controller = FtmsBlePeripheralController(backend, local_name="ProjectAtlas")

    controller.start()

    assert controller.started is True
    assert len(backend.services) == 1
    assert backend.services[0].uuid == FTMS_GATT_PROFILE.service_uuid
    assert backend.advertisement is not None
    assert backend.advertisement.local_name == "ProjectAtlas"
    assert backend.advertisement.service_uuids == (FTMS_GATT_PROFILE.service_uuid,)


def test_ftms_ble_peripheral_notify_after_start():
    backend = MockBleBackend()
    controller = FtmsBlePeripheralController(backend)

    controller.start()
    payload = controller.notify_rower_data({"spm": 24, "watts": 100, "stroke_count": 3})

    assert len(payload) == 14
    assert len(backend.notifications) == 1
    assert backend.notifications[0].characteristic_uuid == FTMS_GATT_PROFILE.rower_data_uuid


def test_ftms_ble_peripheral_rejects_notify_before_start():
    backend = MockBleBackend()
    controller = FtmsBlePeripheralController(backend)

    try:
        controller.notify_rower_data({"spm": 24})
    except RuntimeError as exc:
        assert "must be started" in str(exc)
    else:
        raise AssertionError("Expected notify before start rejection")


def test_ftms_ble_peripheral_stop_disables_advertising():
    backend = MockBleBackend()
    controller = FtmsBlePeripheralController(backend)

    controller.start()
    controller.stop()

    assert controller.started is False
    assert backend.advertisement is None
