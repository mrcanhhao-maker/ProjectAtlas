from engine.ftms_bridge_pipeline import FtmsBridgePipeline
from engine.ftms_bridge_publisher import FtmsBridgePublisher
from engine.ftms_bridge_serial import FtmsBridgeSerialCodec
from engine.ftms_bridge_transport import InMemoryFtmsBridgeTransport


def test_bridge_pipeline_publishes_runtime_rower_state_packet():
    transport = InMemoryFtmsBridgeTransport(packets=[])
    publisher = FtmsBridgePublisher(transport=transport)
    pipeline = FtmsBridgePipeline(publisher=publisher)

    pipeline.publish_runtime_rower_state(
        {
            "elapsed_seconds": 40,
            "spm": 30,
            "stroke_count": 18,
            "power": 220,
            "distance": 160,
            "calories": 12,
        }
    )

    decoded = FtmsBridgeSerialCodec().decode(transport.packets[0])

    assert publisher.published_count == 1
    assert decoded.elapsed_seconds == 40
    assert decoded.stroke_rate_spm == 30
    assert decoded.stroke_count == 18
    assert decoded.instant_power_watts == 220
    assert decoded.total_distance_meters == 160
    assert decoded.calories_kcal == 12
