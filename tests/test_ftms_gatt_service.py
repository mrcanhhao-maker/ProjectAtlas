from engine.ftms_constants import FTMS_GATT_PROFILE
from engine.ftms_gatt_service import build_ftms_gatt_service


def test_build_ftms_gatt_service_uses_verified_profile():
    service = build_ftms_gatt_service()

    assert service.uuid == FTMS_GATT_PROFILE.service_uuid
    assert len(service.characteristics) == 3


def test_build_ftms_gatt_service_contains_rower_data_notify():
    service = build_ftms_gatt_service()
    chars = {char.uuid: char for char in service.characteristics}

    rower_data = chars[FTMS_GATT_PROFILE.rower_data_uuid]

    assert rower_data.properties == ("notify",)


def test_build_ftms_gatt_service_contains_feature_read():
    service = build_ftms_gatt_service()
    chars = {char.uuid: char for char in service.characteristics}

    feature = chars[FTMS_GATT_PROFILE.fitness_machine_feature_uuid]

    assert feature.properties == ("read",)
