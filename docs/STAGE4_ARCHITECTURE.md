# ProjectAtlas Stage 4 Architecture

Version: Alpha14.0

Status: STARTED

Goal:
Prepare BLE GATT Server architecture for exposing ProjectAtlas as a virtual FTMS rowing machine.

Stage 4 principle:
Do not directly bind ProjectAtlas to one Bluetooth implementation at the beginning.
First create a backend abstraction, then test with a mock backend, then add macOS CoreBluetooth.

Confirmed direction:
- FTMS payload pipeline is complete from Stage 3.
- FTMS service and characteristic UUIDs are verified.
- Rower Data payload is ready to be sent as a BLE notify characteristic.
- BLE GATT server is not implemented yet.

Likely macOS backend:
- CoreBluetooth CBPeripheralManager
- Python bridge through PyObjC
- Native Swift bridge remains fallback if Python/CoreBluetooth is unstable.

Required Stage 4 components:
1. BLE backend interface.
2. Mock BLE backend for tests.
3. FTMS GATT service model.
4. Rower Data notify pipeline.
5. macOS CoreBluetooth backend investigation.
6. MyWhoosh pairing experiment only after mock path is stable.

Risk:
MacBook BLE peripheral behavior may depend on macOS permissions, CoreBluetooth event loop, advertising support, and app packaging.

Decision:
Alpha14.1 must create backend abstraction only.
