from __future__ import annotations

import json

from engine.ftms_constants import FTMS_GATT_PROFILE, FTMS_ROWER_DATA_UUID_16, FTMS_SERVICE_UUID_16
from engine.ftms_decoder import FtmsRowingMeasurementDecoder
from engine.ftms_encoder import FtmsRowingMeasurementEncoder
from engine.ftms_mapper import FtmsMapper
from engine.ftms_payload import FtmsPayloadBuilder
from engine.ftms_validator import FtmsPayloadValidator


def main() -> None:
    sample = {
        "elapsed_time_s": 45,
        "spm": 28,
        "stroke_count": 21,
        "distance_m": 180,
        "speed_mps": 3.0,
        "pace_500m_s": 166,
        "watts": 190,
        "moving": True,
    }

    mapper = FtmsMapper()
    encoder = FtmsRowingMeasurementEncoder()
    decoder = FtmsRowingMeasurementDecoder()
    validator = FtmsPayloadValidator()
    builder = FtmsPayloadBuilder()

    measurement = mapper.map_virtual_rower(sample)
    payload = builder.build_rowing_measurement(sample)
    decoded = decoder.decode(payload)
    validation = validator.validate_rowing_measurement(payload)

    checks = {
        "mapper": measurement.power_watts == 190 and measurement.stroke_count == 21,
        "encoder": isinstance(payload, bytes) and len(payload) == 14,
        "decoder": decoded["power_watts"] == 190 and decoded["stroke_count"] == 21,
        "validator": validation.ok is True,
        "payload_builder": encoder.encode(measurement) == payload,
        "ftms_constants": FTMS_SERVICE_UUID_16 == 0x1826 and FTMS_ROWER_DATA_UUID_16 == 0x2AD1,
    }

    status = "PASS" if all(checks.values()) else "FAIL"

    print(json.dumps(
        {
            "stage": "stage3",
            "version": "Alpha13.10",
            "status": status,
            "scope": "FTMS preparation only; BLE GATT server not started",
            "checks": checks,
            "payload_hex": payload.hex(" "),
            "decoded": decoded,
            "ftms_gatt_profile": FTMS_GATT_PROFILE.__dict__,
            "next": "Add BLE GATT server planning docs after FTMS constants are locked.",
        },
        indent=2,
        ensure_ascii=False,
    ))

    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
