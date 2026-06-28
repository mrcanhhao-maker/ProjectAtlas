from engine.ftms_constants import FTMS_GATT_PROFILE
from engine.ftms_gatt_service import build_ftms_gatt_service


def test_ftms_feature_characteristic_has_static_read_value():
    service = build_ftms_gatt_service()

    feature = next(
        characteristic
        for characteristic in service.characteristics
        if characteristic.uuid == FTMS_GATT_PROFILE.fitness_machine_feature_uuid
    )

    assert "read" in feature.properties
    assert feature.value == bytes.fromhex("0000000000000000")
