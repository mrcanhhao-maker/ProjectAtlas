from __future__ import annotations

import json
import platform


def main() -> None:
    result = {
        "tool": "macos_ble_capability_check",
        "version": "Alpha14.7",
        "system": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "pyobjc_available": False,
        "corebluetooth_available": False,
        "cbperipheralmanager_available": False,
        "status": "FAIL",
        "next": "Install or verify PyObjC/CoreBluetooth before native BLE backend.",
    }

    try:
        import objc  # type: ignore

        result["pyobjc_available"] = True
        result["pyobjc_version"] = getattr(objc, "__version__", "unknown")
    except Exception as exc:
        result["pyobjc_error"] = str(exc)

    try:
        import CoreBluetooth  # type: ignore

        result["corebluetooth_available"] = True
        result["cbperipheralmanager_available"] = hasattr(CoreBluetooth, "CBPeripheralManager")
    except Exception as exc:
        result["corebluetooth_error"] = str(exc)

    if (
        result["system"] == "Darwin"
        and result["pyobjc_available"]
        and result["corebluetooth_available"]
        and result["cbperipheralmanager_available"]
    ):
        result["status"] = "PASS"
        result["next"] = "Create guarded CoreBluetooth backend skeleton."

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
