# ProjectAtlas Stage 5 — FTMS Architecture Decision

## Current blocker

CoreBluetooth runtime reports:

- powered_on
- service 1826 added
- characteristics 2AD1, 2ACC, 2ADA present
- startAdvertising OK
- isAdvertising True

But LightBlue on iPhone does not discover ProjectAtlas FTMS GATT.
It sees macOS system BLE identity instead.

## Rule

Do not continue FTMS notify/read/write callbacks until a central can discover and subscribe to ProjectAtlas FTMS characteristics.

## Stage 5 decision paths

1. Continue CoreBluetooth/PyObjC only if an external BLE central can discover:
   - FTMS service 1826
   - Indoor Rowing Data 2AD1
   - Fitness Machine Feature 2ACC
   - Fitness Machine Status 2ADA

2. If macOS prevents reliable user-space BLE peripheral exposure, move FTMS peripheral role to ESP32.

## Preferred fallback architecture

MacBook:
- camera
- pose AI
- stroke engine
- power/distance/pace/calorie calculation
- sends rower metrics to bridge

ESP32:
- BLE FTMS Peripheral
- exposes service 1826
- exposes characteristics 2AD1, 2ACC, 2ADA
- notifies MyWhoosh like a real rower

## Non-goals

- Do not replace Vision Engine.
- Do not remove current FTMS encoder/mapper/validator.
- Do not add untested runtime callbacks before discovery works.
