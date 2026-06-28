import pytest

from engine.ftms_bridge_contract import FtmsBridgeMetrics
from engine.ftms_bridge_publisher import FtmsBridgePublisher
from engine.ftms_bridge_transport import InMemoryFtmsBridgeTransport


def test_bridge_publisher_sends_metrics_and_tracks_state():
    transport = InMemoryFtmsBridgeTransport(packets=[])
    publisher = FtmsBridgePublisher(transport=transport)

    metrics = FtmsBridgeMetrics(
        elapsed_seconds=20,
        stroke_rate_spm=29,
        stroke_count=10,
        instant_power_watts=260,
        total_distance_meters=90,
        calories_kcal=8,
    )

    publisher.publish(metrics)

    assert publisher.published_count == 1
    assert publisher.last_metrics == metrics
    assert len(transport.packets) == 1


def test_bridge_publisher_rejects_invalid_metrics_before_transport_send():
    transport = InMemoryFtmsBridgeTransport(packets=[])
    publisher = FtmsBridgePublisher(transport=transport)

    with pytest.raises(ValueError):
        publisher.publish(
            FtmsBridgeMetrics(
                elapsed_seconds=1,
                stroke_rate_spm=999,
                stroke_count=1,
                instant_power_watts=100,
                total_distance_meters=1,
                calories_kcal=1,
            )
        )

    assert publisher.published_count == 0
    assert transport.packets == []
