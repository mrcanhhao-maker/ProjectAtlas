from __future__ import annotations

import struct
from typing import Dict, Any


class FtmsRowingMeasurementDecoder:
    def decode(self, payload: bytes) -> Dict[str, Any]:
        if len(payload) < 14:
            raise ValueError(f"FTMS rowing measurement payload too short: {len(payload)} bytes")

        flags = struct.unpack_from("<H", payload, 0)[0]
        stroke_rate_spm = payload[2] / 2.0
        stroke_count = struct.unpack_from("<H", payload, 3)[0]
        distance_m = payload[5] | (payload[6] << 8) | (payload[7] << 16)
        pace_500m_s = struct.unpack_from("<H", payload, 8)[0]
        power_watts = struct.unpack_from("<h", payload, 10)[0]
        elapsed_time_s = struct.unpack_from("<H", payload, 12)[0]

        return {
            "flags": flags,
            "stroke_rate_spm": stroke_rate_spm,
            "stroke_count": stroke_count,
            "distance_m": distance_m,
            "pace_500m_s": pace_500m_s,
            "power_watts": power_watts,
            "elapsed_time_s": elapsed_time_s,
        }
