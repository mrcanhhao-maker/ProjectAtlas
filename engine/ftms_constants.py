from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


BLUETOOTH_BASE_UUID_SUFFIX = "-0000-1000-8000-00805f9b34fb"


def expand_bluetooth_uuid(short_code: int) -> str:
    if short_code < 0 or short_code > 0xFFFF:
        raise ValueError("Bluetooth 16-bit UUID must be between 0x0000 and 0xFFFF")
    return f"0000{short_code:04x}{BLUETOOTH_BASE_UUID_SUFFIX}"


@dataclass(frozen=True)
class FtmsGattProfile:
    service_uuid: str
    rower_data_uuid: str
    fitness_machine_feature_uuid: str
    fitness_machine_status_uuid: str
    fitness_machine_control_point_uuid: str
    supported_characteristics: Tuple[str, ...]


FTMS_SERVICE_UUID_16 = 0x1826
FTMS_ROWER_DATA_UUID_16 = 0x2AD1
FTMS_FEATURE_UUID_16 = 0x2ACC
FTMS_STATUS_UUID_16 = 0x2ADA
FTMS_CONTROL_POINT_UUID_16 = 0x2AD9

FTMS_GATT_PROFILE = FtmsGattProfile(
    service_uuid=expand_bluetooth_uuid(FTMS_SERVICE_UUID_16),
    rower_data_uuid=expand_bluetooth_uuid(FTMS_ROWER_DATA_UUID_16),
    fitness_machine_feature_uuid=expand_bluetooth_uuid(FTMS_FEATURE_UUID_16),
    fitness_machine_status_uuid=expand_bluetooth_uuid(FTMS_STATUS_UUID_16),
    fitness_machine_control_point_uuid=expand_bluetooth_uuid(FTMS_CONTROL_POINT_UUID_16),
    supported_characteristics=(
        "rower_data",
        "fitness_machine_feature",
        "fitness_machine_status",
        "fitness_machine_control_point",
    ),
)
