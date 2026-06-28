import struct

from engine.ftms_encoder import FtmsRowingMeasurementEncoder
from engine.ftms_mapper import FtmsRowerMeasurement


def test_ftms_encoder_outputs_stable_payload_layout():
    encoder = FtmsRowingMeasurementEncoder()

    payload = encoder.encode(
        FtmsRowerMeasurement(
            elapsed_time_s=12.4,
            stroke_rate_spm=28.5,
            stroke_count=10,
            distance_m=123.4,
            speed_mps=3.2,
            pace_500m_s=156.7,
            power_watts=210,
            moving=True,
        )
    )

    assert len(payload) == 14

    flags = struct.unpack_from("<H", payload, 0)[0]
    assert flags == (
        encoder.FLAG_TOTAL_DISTANCE_PRESENT
        | encoder.FLAG_INSTANTANEOUS_PACE_PRESENT
        | encoder.FLAG_INSTANTANEOUS_POWER_PRESENT
        | encoder.FLAG_ELAPSED_TIME_PRESENT
    )

    assert payload[2] == 57
    assert struct.unpack_from("<H", payload, 3)[0] == 10
    assert payload[5:8] == bytes((123, 0, 0))
    assert struct.unpack_from("<H", payload, 8)[0] == 157
    assert struct.unpack_from("<h", payload, 10)[0] == 210
    assert struct.unpack_from("<H", payload, 12)[0] == 12


def test_ftms_encoder_clamps_numeric_ranges():
    encoder = FtmsRowingMeasurementEncoder()

    payload = encoder.encode(
        FtmsRowerMeasurement(
            elapsed_time_s=999999,
            stroke_rate_spm=999,
            stroke_count=999999,
            distance_m=999999999,
            speed_mps=0,
            pace_500m_s=999999,
            power_watts=999999,
            moving=True,
        )
    )

    assert payload[2] == 255
    assert struct.unpack_from("<H", payload, 3)[0] == 65535
    assert payload[5:8] == bytes((255, 255, 255))
    assert struct.unpack_from("<H", payload, 8)[0] == 65535
    assert struct.unpack_from("<h", payload, 10)[0] == 32767
    assert struct.unpack_from("<H", payload, 12)[0] == 65535
