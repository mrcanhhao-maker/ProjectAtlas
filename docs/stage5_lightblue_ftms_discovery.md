# Stage 5 — LightBlue FTMS Discovery Update

## Result

LightBlue on iPhone successfully connected to the macOS BLE peripheral named:

- mrcanhhao

After connection, LightBlue discovered ProjectAtlas FTMS GATT:

- Fitness Machine Service: 00001826-0000-1000-8000-00805F9B34FB
- Indoor Rowing Data: 00002AD1-0000-1000-8000-00805F9B34FB
- Fitness Machine Feature: 00002ACC-0000-1000-8000-00805F9B34FB
- Fitness Machine Status: 00002ADA-0000-1000-8000-00805F9B34FB

## Correction

Previous assumption was incomplete:

- ProjectAtlas FTMS was not visible by expected local name.
- But FTMS GATT is discoverable after connecting to the macOS advertised peripheral.

## Updated decision

Do not move to ESP32 yet.

Continue laptop-only CoreBluetooth path.

## Next validation

1. Confirm central subscription to 2AD1.
2. Send Indoor Rowing Data notify payload.
3. Confirm LightBlue receives notifications.
4. Test MyWhoosh connection.
