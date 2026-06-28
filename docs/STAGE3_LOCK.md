# ProjectAtlas Stage 3 Lock

Version: Alpha13.12

Status: LOCKED

Stage 3 scope:
FTMS preparation only.

Completed:
- FTMS Mapper
- FTMS Rowing Measurement Encoder
- FTMS Payload Builder
- FTMS Rowing Measurement Decoder
- FTMS Payload Validator
- FTMS Payload Debug Tool
- Stage 3 Healthcheck
- Verified FTMS Constants
- BLE Implementation Plan

Verified FTMS UUIDs:
- Fitness Machine Service: 0x1826
- Rower Data: 0x2AD1
- Fitness Machine Feature: 0x2ACC
- Fitness Machine Status: 0x2ADA

Not included in Stage 3:
- BLE GATT server
- Bluetooth advertising
- MyWhoosh connection
- Native macOS CoreBluetooth implementation

Stage 4 entry condition:
Only begin BLE work after Stage 3 healthcheck and all FTMS tests pass.

Current stage result:
PASS.
