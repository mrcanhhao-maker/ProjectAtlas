import struct

from engine.ftms_payload import FtmsPayloadBuilder
from engine.ftms_mapper import FtmsRowerMeasurement


def test_ftms_payload_builder_maps_and_encodes_virtual_rower_data():
    builder = FtmsPayloadBuilder()

    payload = builder.build_rowing_measurement(
        {
            "elapsed_time_s": 20,
            "spm": 30,
            "stroke_count": 12,
            "distance_m": 100,
            "speed_mps": 2.5,
            "pace_500m_s": 200,
            "watts": 150,
            "moving": True,
        }
    )

    assert len(payload) == 14
    assert payload[2] == 60
    assert struct.unpack_from("<H", payload, 3)[0] == 12
    assert payload[5:8] == bytes((100, 0, 0))
    assert struct.unpack_from("<H", payload, 8)[0] == 200
    assert struct.unpack_from("<h", payload, 10)[0] == 150
    assert struct.unpack_from("<H", payload, 12)[0] == 20


def test_ftms_payload_builder_exposes_mapped_measurement_for_debugging():
    builder = FtmsPayloadBuilder()

    measurement = builder.map_rowing_measurement({"spm": 18, "watts": 80})

    assert isinstance(measurement, FtmsRowerMeasurement)
    assert measurement.stroke_rate_spm == 18
    assert measurement.power_watts == 80
    assert measurement.moving is True
