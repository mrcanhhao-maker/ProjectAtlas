# ProjectAtlas Alpha14 CoreBluetooth Interop Note

## Verified working

- CBPeripheralManager reaches powered_on state.
- FTMS service 0x1826 is successfully registered.
- FTMS characteristics are present:
  - 0x2AD1 Rower Data notify
  - 0x2ACC Fitness Machine Feature read
  - 0x2ADA Fitness Machine Status notify
- Advertising starts without CoreBluetooth errors.
- Advertising payload includes FTMS service UUID 0x1826.
- CBPeripheralManager.isAdvertising() returns true.

## Observed interoperability issue

LightBlue on iPhone connects to the Mac's system BLE/GATT identity instead of the ProjectAtlas FTMS GATT service.

LightBlue shows:
- Device Information
- Apple Inc.
- MacBookPro16,2
- random 128-bit service UUIDs

LightBlue does not show:
- 0x1826
- 0x2AD1
- 0x2ACC
- 0x2ADA

## Engineering conclusion

The Python/PyObjC/CoreBluetooth implementation is internally correct up to service registration and advertising.

The remaining blocker is external interoperability: iOS/LightBlue is discovering or connecting to macOS system BLE services rather than the CBPeripheralManager-published FTMS service.

Do not continue adding FTMS notify/read/write callbacks until a central can actually discover and subscribe to the ProjectAtlas FTMS characteristics.

## Next direction

Evaluate one of these paths:

1. Native macOS app wrapper with proper CoreBluetooth entitlement/runtime behavior.
2. BLE peripheral hardware bridge such as ESP32 running FTMS GATT.
3. Continue Python only if another central confirms discovery of ProjectAtlas FTMS service 0x1826.
