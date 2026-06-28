from engine.ftms_constants import FTMS_GATT_PROFILE
from engine.ftms_gatt_service import build_ftms_gatt_service
from engine.ftms_notify_pipeline import FtmsRowerNotifyPipeline
from engine.mock_ble_backend import MockBleBackend


def test_ftms_notify_pipeline_sends_valid_rower_payload_to_backend():
    backend = MockBleBackend()
    backend.add_service(build_ftms_gatt_service())

    pipeline = FtmsRowerNotifyPipeline(backend)
    payload = pipeline.notify_rower_data(
        {
            "elapsed_time_s": 10,
            "spm": 24,
            "stroke_count": 5,
            "distance_m": 32,
            "speed_mps": 2.0,
            "pace_500m_s": 220,
            "watts": 95,
            "moving": True,
        }
    )

    assert len(payload) == 14
    assert len(backend.notifications) == 1
    assert backend.notifications[0].characteristic_uuid == FTMS_GATT_PROFILE.rower_data_uuid
    assert backend.notifications[0].payload == payload


def test_ftms_notify_pipeline_requires_registered_rower_characteristic():
    backend = MockBleBackend()
    pipeline = FtmsRowerNotifyPipeline(backend)

    try:
        pipeline.notify_rower_data({"spm": 20, "watts": 50})
    except ValueError as exc:
        assert "Unknown BLE characteristic" in str(exc)
    else:
        raise AssertionError("Expected missing characteristic rejection")
