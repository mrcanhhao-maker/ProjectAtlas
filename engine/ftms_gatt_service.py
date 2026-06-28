from __future__ import annotations

from engine.ble_backend import BleCharacteristic, BleService
from engine.ftms_constants import FTMS_GATT_PROFILE


def build_ftms_gatt_service() -> BleService:
    return BleService(
        uuid=FTMS_GATT_PROFILE.service_uuid,
        characteristics=(
            BleCharacteristic(
                uuid=FTMS_GATT_PROFILE.rower_data_uuid,
                properties=("notify",),
            ),
            BleCharacteristic(
                uuid=FTMS_GATT_PROFILE.fitness_machine_feature_uuid,
                properties=("read",),
                value=bytes.fromhex("0000000000000000"),
            ),
            BleCharacteristic(
                uuid=FTMS_GATT_PROFILE.fitness_machine_status_uuid,
                properties=("notify",),
            ),
            BleCharacteristic(
                uuid=FTMS_GATT_PROFILE.fitness_machine_control_point_uuid,
                properties=("write", "indicate"),
            ),
        ),
    )
