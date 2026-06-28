import pytest

from engine.ftms_bridge_contract import FtmsBridgeMetrics
from engine.ftms_bridge_serial import FtmsBridgeSerialCodec


def test_bridge_serial_codec_round_trips_metrics():
    codec = FtmsBridgeSerialCodec()
    metrics = FtmsBridgeMetrics(
        elapsed_seconds=12,
        stroke_rate_spm=30,
        stroke_count=6,
        instant_power_watts=210,
        total_distance_meters=55,
        calories_kcal=4,
    )

    encoded = codec.encode(metrics)
    decoded = codec.decode(encoded)

    assert encoded.endswith(b"\n")
    assert decoded == metrics


def test_bridge_serial_codec_rejects_invalid_json():
    with pytest.raises(ValueError):
        FtmsBridgeSerialCodec().decode(b"not-json\n")


def test_bridge_serial_codec_rejects_out_of_range_payload():
    with pytest.raises(ValueError):
        FtmsBridgeSerialCodec().decode(
            b'{"elapsed_seconds":1,"stroke_rate_spm":999,'
            b'"stroke_count":1,"instant_power_watts":100,'
            b'"total_distance_meters":1,"calories_kcal":1}\n'
        )
