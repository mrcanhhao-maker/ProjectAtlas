from __future__ import annotations

import json

from engine.ble_backend_factory import BleBackendFactory
from engine.ftms_ble_peripheral import FtmsBlePeripheralController
from engine.ftms_constants import FTMS_GATT_PROFILE
from engine.ftms_decoder import FtmsRowingMeasurementDecoder


def main() -> None:
    selection = BleBackendFactory().create(prefer_native=True)
    backend = selection.backend

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
        "backend_factory_used": selection.name in {"mock", "corebluetooth_pending"},
        "backend_selected": backend is not None,
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
            "version": "Alpha14.10",
            "status": status,
            "scope": "BLE architecture through backend factory; CoreBluetooth backend not implemented yet",
            "backend": {
                "name": selection.name,
                "reason": selection.reason,
                "native_ready": selection.native_ready,
            },
            "checks": checks,
            "payload_hex": payload.hex(" "),
            "decoded": decoded,
            "next": "Implement guarded CoreBluetooth backend skeleton.",
        },
        indent=2,
        ensure_ascii=False,
    ))

    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
