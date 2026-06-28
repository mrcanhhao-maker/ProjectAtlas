import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from engine.ftms_bridge_pipeline import FtmsBridgePipeline
from engine.ftms_bridge_publisher import FtmsBridgePublisher
from engine.ftms_bridge_serial import FtmsBridgeSerialCodec
from engine.ftms_bridge_transport import InMemoryFtmsBridgeTransport


def main():
    transport = InMemoryFtmsBridgeTransport(packets=[])
    publisher = FtmsBridgePublisher(transport=transport)
    pipeline = FtmsBridgePipeline(publisher=publisher)

    pipeline.publish_runtime_rower_state(
        {
            "elapsed_seconds": 60,
            "spm": 28,
            "stroke_count": 30,
            "power": 185,
            "distance": 250,
            "calories": 18,
        }
    )

    packet = transport.packets[0]
    decoded = FtmsBridgeSerialCodec().decode(packet)

    print(packet.decode("utf-8").strip())
    print(decoded)


if __name__ == "__main__":
    main()
