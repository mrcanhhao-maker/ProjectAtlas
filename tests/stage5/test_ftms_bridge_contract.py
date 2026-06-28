import pytest

from engine.ftms_bridge_contract import (
    FtmsBridgeMetrics,
    FtmsBridgeMetricsValidator,
)


def valid_metrics():
    return FtmsBridgeMetrics(
        elapsed_seconds=10,
        stroke_rate_spm=28,
        stroke_count=5,
        instant_power_watts=180,
        total_distance_meters=42,
        calories_kcal=3,
    )


def test_bridge_metrics_accept_valid_rower_payload():
    FtmsBridgeMetricsValidator().validate(valid_metrics())


@pytest.mark.parametrize(
    "field,value",
    [
        ("elapsed_seconds", -1),
        ("stroke_rate_spm", -1),
        ("stroke_rate_spm", 121),
        ("stroke_count", -1),
        ("instant_power_watts", -1),
        ("instant_power_watts", 2001),
        ("total_distance_meters", -1),
        ("calories_kcal", -1),
    ],
)
def test_bridge_metrics_reject_invalid_values(field, value):
    data = valid_metrics().__dict__.copy()
    data[field] = value

    with pytest.raises(ValueError):
        FtmsBridgeMetricsValidator().validate(FtmsBridgeMetrics(**data))
