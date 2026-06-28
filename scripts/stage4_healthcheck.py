from __future__ import annotations

import json

from engine.ftms_ble_peripheral import FtmsBlePeripheralController
from engine.ftms_constants import FTMS_GATT_PROFILE
from engine.ftms_decoder import FtmsRowingMeasurementDecoder
from engine.mock_ble_backend import MockBleBackend


def main() -> None:
    backend = MockBleBackend()
    controller = FtmsBlePeripheralController(backend, local_name="ProjectAtlas")
    decoder = FtmsRowingMeasurementDecoder()

    controller.start()

    payload = controller.notify_rower_data(
        {
            "elapsed_time_s": 12,
            "spm": 24,
            "stroke_count": 6,
            "distance_m": 40,
            "speed_mps": 2.1,
            "pace_500m_s": 238,
            "watts": 105,
            "moving": True,
        }
    )

    decoded = decoder.decode(payload)

    checks = {
        "service_registered": len(backend.services) == 1 and backend.services[0].uuid == FTMS_GATT_PROFILE.service_uuid,
        "advertising_started": backend.advertisement is not None and backend.advertisement.local_name == "ProjectAtlas",
        "rower_data_notified": len(backend.notifications) == 1 and backend.notifications[0].characteristic_uuid == FTMS_GATT_PROFILE.rower_data_uuid,
        "payload_len": len(payload) == 14,
        "decoded_power": decoded["power_watts"] == 105,
        "decoded_strokes": decoded["stroke_count"] == 6,
    }

    controller.stop()
    checks["advertising_stopped"] = backend.advertisement is None

    status = "PASS" if all(checks.values()) else "FAIL"

    print(json.dumps(
        {
            "stage": "stage4",
            "version": "Alpha14.6",
            "status": status,
            "scope": "BLE architecture with mock backend only; no CoreBluetooth yet",
            "checks": checks,
            "payload_hex": payload.hex(" "),
            "decoded": decoded,
            "next": "Investigate macOS CoreBluetooth peripheral backend.",
        },
        indent=2,
        ensure_ascii=False,
    ))

    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
