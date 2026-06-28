# Stage 6.2 – MyWhoosh FTMS Research

## Checkpoint

- Branch: alpha10
- Stage 5 passed and pushed.
- Stage 6 added FTMS Control Point 2AD9.
- Stage 6.1 removed BLE Appearance from CoreBluetooth advertising because it caused runtime SIGABRT.
- Current pytest result: 92 passed.
- Runtime stable:
  - state=powered_on
  - services=1
  - advertising=True
  - errors=[]
- LightBlue sees device `mrcanhhao`.
- LightBlue can discover FTMS service 1826 and characteristics 2AD1 / 2ACC / 2ADA / 2AD9.
- LightBlue can subscribe to 2AD1 notifications.
- MyWhoosh still reports No Device Found.

## Research conclusion

MyWhoosh version 5.8.0 supports FTMS-compatible rowing machines, not only Concept2 rowers.

The most likely blocker is advertisement-level filtering.

The FTMS specification defines Service Advertising Data so a client can determine the fitness machine type before connecting. For a rower, the FTMS Service Data must identify:
- Fitness Machine Service UUID: 0x1826
- Fitness Machine Available flag: true
- Fitness Machine Type bit 4: Rower Supported

macOS CoreBluetooth peripheral advertising is limited to:
- CBAdvertisementDataLocalNameKey
- CBAdvertisementDataServiceUUIDsKey

Therefore laptop-only CoreBluetooth can expose the correct GATT service after connection, but it cannot fully advertise FTMS Service Data as a real FTMS rower would.

## Working hypothesis

LightBlue succeeds because it can connect and discover GATT characteristics manually.

MyWhoosh likely filters scan results before connecting and requires FTMS Service Data that marks the advertiser as an available rower.

## Decision

Do not add random FTMS characteristics or payload fields yet.

Next technical validation:
1. Capture LightBlue advertisement view and confirm whether Service Data for UUID 1826 is absent.
2. If absent, treat macOS CoreBluetooth advertisement limitation as the current MyWhoosh discovery blocker.
3. Continue laptop-only only if a CoreBluetooth-compatible workaround is found.
4. Do not use ESP32.
