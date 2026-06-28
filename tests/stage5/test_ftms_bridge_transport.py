from engine.ftms_bridge_contract import FtmsBridgeMetrics
from engine.ftms_bridge_serial import FtmsBridgeSerialCodec
from engine.ftms_bridge_transport import InMemoryFtmsBridgeTransport


def test_in_memory_bridge_transport_sends_encoded_metrics_packet():
    transport = InMemoryFtmsBridgeTransport(packets=[])
    metrics = FtmsBridgeMetrics(
        elapsed_seconds=15,
        stroke_rate_spm=31,
        stroke_count=8,
        instant_power_watts=240,
        total_distance_meters=70,
        calories_kcal=6,
    )

    transport.send(metrics)

    assert len(transport.packets) == 1
    assert FtmsBridgeSerialCodec().decode(transport.packets[0]) == metrics
