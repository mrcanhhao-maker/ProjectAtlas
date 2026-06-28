from __future__ import annotations

import signal
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from engine.corebluetooth_backend import CoreBluetoothBackend
from engine.ftms_ble_peripheral import FtmsBlePeripheralController


running = True


def stop(_signum, _frame):
    global running
    running = False


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

backend = CoreBluetoothBackend()
backend.peripheral_manager.pump_run_loop(1.0)

controller = FtmsBlePeripheralController(backend, local_name="mrcanhhao")
controller.start()

print("ProjectAtlas FTMS BLE peripheral running")
print("Open LightBlue/MyWhoosh and scan for mrcanhhao")
print("Press Ctrl+C to stop")

try:
    while running:
        backend.peripheral_manager.pump_run_loop(0.25)
        print(
            "state=", backend.peripheral_manager.state_name,
            "services=", backend.peripheral_manager.added_service_count,
            "advertising=", backend.peripheral_manager.advertising_started,
            "errors=", backend.peripheral_manager.service_errors + backend.peripheral_manager.advertising_errors,
        )
        time.sleep(1.0)
finally:
    controller.stop()
    print("ProjectAtlas FTMS BLE peripheral stopped")
