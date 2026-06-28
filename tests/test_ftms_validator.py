from engine.ftms_encoder import FtmsRowingMeasurementEncoder
from engine.ftms_mapper import FtmsRowerMeasurement
from engine.ftms_validator import FtmsPayloadValidator


def test_ftms_validator_accepts_encoder_payload():
    encoder = FtmsRowingMeasurementEncoder()
    validator = FtmsPayloadValidator()

    payload = encoder.encode(
        FtmsRowerMeasurement(
            elapsed_time_s=10,
            stroke_rate_spm=24,
            stroke_count=4,
            distance_m=30,
            speed_mps=2,
            pace_500m_s=220,
            power_watts=90,
            moving=True,
        )
    )

    result = validator.validate_rowing_measurement(payload)

    assert result.ok is True
    assert result.errors == []


def test_ftms_validator_rejects_wrong_length():
    validator = FtmsPayloadValidator()

    result = validator.validate_rowing_measurement(b"\x00\x00")

    assert result.ok is False
    assert "payload length must be 14 bytes" in result.errors[0]


def test_ftms_validator_rejects_non_bytes():
    validator = FtmsPayloadValidator()

    result = validator.validate_rowing_measurement("bad")  # type: ignore[arg-type]

    assert result.ok is False
    assert result.errors == ["payload must be bytes"]
