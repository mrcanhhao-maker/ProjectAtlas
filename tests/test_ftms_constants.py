from engine.ftms_constants import (
    FTMS_FEATURE_UUID_16,
    FTMS_GATT_PROFILE,
    FTMS_ROWER_DATA_UUID_16,
    FTMS_SERVICE_UUID_16,
    FTMS_STATUS_UUID_16,
    expand_bluetooth_uuid,
)


def test_expand_bluetooth_uuid_uses_standard_base_uuid():
    assert expand_bluetooth_uuid(0x1826) == "00001826-0000-1000-8000-00805f9b34fb"
    assert expand_bluetooth_uuid(0x2AD1) == "00002ad1-0000-1000-8000-00805f9b34fb"


def test_expand_bluetooth_uuid_rejects_invalid_short_code():
    try:
        expand_bluetooth_uuid(0x10000)
    except ValueError as exc:
        assert "16-bit UUID" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_ftms_verified_short_uuids_are_locked():
    assert FTMS_SERVICE_UUID_16 == 0x1826
    assert FTMS_ROWER_DATA_UUID_16 == 0x2AD1
    assert FTMS_FEATURE_UUID_16 == 0x2ACC
    assert FTMS_STATUS_UUID_16 == 0x2ADA


def test_ftms_gatt_profile_contains_verified_characteristics():
    profile = FTMS_GATT_PROFILE

    assert profile.service_uuid == "00001826-0000-1000-8000-00805f9b34fb"
    assert profile.rower_data_uuid == "00002ad1-0000-1000-8000-00805f9b34fb"
    assert profile.fitness_machine_feature_uuid == "00002acc-0000-1000-8000-00805f9b34fb"
    assert profile.fitness_machine_status_uuid == "00002ada-0000-1000-8000-00805f9b34fb"
    assert profile.fitness_machine_control_point_uuid == "00002ad9-0000-1000-8000-00805f9b34fb"
    assert profile.supported_characteristics == (
        "rower_data",
        "fitness_machine_feature",
        "fitness_machine_status",
        "fitness_machine_control_point",
    )
