# Stage 5 LightBlue Notify Validation

ProjectAtlas successfully exposes a laptop-only CoreBluetooth FTMS peripheral.

Validated with LightBlue:

- FTMS service `00001826-0000-1000-8000-00805F9B34FB` discovered.
- Indoor Rowing Data characteristic `00002AD1-0000-1000-8000-00805F9B34FB` discovered.
- LightBlue connects to the peripheral.
- LightBlue subscribes to `2AD1`.
- `2AD1` notify values are received continuously.
- CoreBluetooth read requests are handled for readable FTMS characteristics.

Observed notified values include:

```text
0x2C08301900300000000000001800
0x2C08301A00320000000000001900
0x2C08301B00340000000000001A00
Status:

LightBlue FTMS discovery, subscription, and notification validation passed.

Next step:

Test ProjectAtlas directly with MyWhoosh as a virtual FTMS rowing machine.
