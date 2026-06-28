# ProjectAtlas Stage 3 BLE Plan

Version: Alpha13.11

Goal:
Prepare ProjectAtlas for a future BLE GATT server that exposes FTMS rowing data to compatible apps.

Current confirmed FTMS profile:
- Fitness Machine Service UUID: 00001826-0000-1000-8000-00805f9b34fb
- Rower Data UUID: 00002ad1-0000-1000-8000-00805f9b34fb
- Fitness Machine Feature UUID: 00002acc-0000-1000-8000-00805f9b34fb
- Fitness Machine Status UUID: 00002ada-0000-1000-8000-00805f9b34fb

Current completed software path:
Camera / VirtualRowerEngine
-> FTMS Mapper
-> FTMS Rowing Measurement
-> FTMS Encoder
-> FTMS Payload Validator
-> Future BLE notify characteristic

Stage 4 entry rule:
Do not start BLE GATT server until Stage 3 is locked and payload tests remain passing.

Stage 4 planned order:
1. Create BLE backend abstraction.
2. Add mock BLE peripheral for tests.
3. Add FTMS service model.
4. Add Rower Data notify pipeline.
5. Add macOS BLE capability investigation.
6. Only then test with MyWhoosh.

Important:
MacBook Bluetooth support for acting as a BLE peripheral may require native macOS CoreBluetooth code or a separate BLE-capable device. This project must verify that before promising direct MyWhoosh connection.
