from dataclasses import dataclass

from engine.ftms_bridge_adapter import FtmsBridgeMetricsAdapter
from engine.ftms_bridge_publisher import FtmsBridgePublisher


@dataclass
class FtmsBridgePipeline:
    publisher: FtmsBridgePublisher

    def __post_init__(self):
        self.adapter = FtmsBridgeMetricsAdapter()

    def publish_runtime_rower_state(self, state: dict) -> None:
        metrics = self.adapter.from_runtime_rower_state(state)
        self.publisher.publish(metrics)
