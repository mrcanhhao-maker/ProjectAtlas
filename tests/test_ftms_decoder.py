from engine.ftms_decoder import FtmsRowingMeasurementDecoder
from engine.ftms_encoder import FtmsRowingMeasurementEncoder
from engine.ftms_mapper import FtmsRowerMeasurement


def test_ftms_decoder_roundtrip_from_encoder():
    encoder = FtmsRowingMeasurementEncoder()
    decoder = FtmsRowingMeasurementDecoder()

    payload = encoder.encode(
        FtmsRowerMeasurement(
            elapsed_time_s=31,
            stroke_rate_spm=27.5,
            stroke_count=15,
            distance_m=130,
            speed_mps=2.9,
            pace_500m_s=172,
            power_watts=175,
            moving=True,
        )
    )

    decoded = decoder.decode(payload)

    assert decoded["stroke_rate_spm"] == 27.5
    assert decoded["stroke_count"] == 15
    assert decoded["distance_m"] == 130
    assert decoded["pace_500m_s"] == 172
    assert decoded["power_watts"] == 175
    assert decoded["elapsed_time_s"] == 31


def test_ftms_decoder_rejects_short_payload():
    decoder = FtmsRowingMeasurementDecoder()

    try:
        decoder.decode(b"\x00\x00")
    except ValueError as exc:
        assert "too short" in str(exc)
    else:
        raise AssertionError("Expected ValueError for short FTMS payload")
