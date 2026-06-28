from __future__ import annotations

import json

from engine.ftms_payload import FtmsPayloadBuilder


def main() -> None:
    sample = {
        "elapsed_time_s": 30,
        "spm": 26,
        "stroke_count": 14,
        "distance_m": 120,
        "speed_mps": 2.8,
        "pace_500m_s": 179,
        "watts": 165,
        "moving": True,
    }

    builder = FtmsPayloadBuilder()
    measurement = builder.map_rowing_measurement(sample)
    payload = builder.build_rowing_measurement(sample)

    print(json.dumps(
        {
            "tool": "ftms_payload_debug",
            "stage": "Alpha13.4",
            "input": sample,
            "measurement": measurement.__dict__,
            "payload_len": len(payload),
            "payload_hex": payload.hex(" "),
        },
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
