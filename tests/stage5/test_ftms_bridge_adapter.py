import pytest

from engine.ftms_bridge_adapter import FtmsBridgeMetricsAdapter
from engine.ftms_bridge_contract import FtmsBridgeMetrics


def test_bridge_adapter_maps_runtime_rower_state_to_bridge_metrics():
    metrics = FtmsBridgeMetricsAdapter().from_runtime_rower_state(
        {
            "elapsed_seconds": 33.2,
            "spm": 27.6,
            "stroke_count": 14,
            "power": 188.4,
            "distance": 123.7,
            "calories": 9.2,
        }
    )

    assert metrics == FtmsBridgeMetrics(
        elapsed_seconds=33,
        stroke_rate_spm=28,
        stroke_count=14,
        instant_power_watts=188,
        total_distance_meters=124,
        calories_kcal=9,
    )


def test_bridge_adapter_rejects_missing_runtime_field():
    with pytest.raises(KeyError):
        FtmsBridgeMetricsAdapter().from_runtime_rower_state(
            {
                "elapsed_seconds": 1,
                "spm": 20,
                "stroke_count": 1,
                "power": 100,
                "distance": 10,
            }
        )


def test_bridge_adapter_rejects_none_runtime_field():
    with pytest.raises(ValueError):
        FtmsBridgeMetricsAdapter().from_runtime_rower_state(
            {
                "elapsed_seconds": 1,
                "spm": None,
                "stroke_count": 1,
                "power": 100,
                "distance": 10,
                "calories": 1,
            }
        )
