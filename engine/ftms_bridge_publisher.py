from dataclasses import dataclass

from engine.ftms_bridge_contract import (
    FtmsBridgeMetrics,
    FtmsBridgeMetricsValidator,
)
from engine.ftms_bridge_transport import FtmsBridgeTransport


@dataclass
class FtmsBridgePublisher:
    transport: FtmsBridgeTransport

    def __post_init__(self):
        self.validator = FtmsBridgeMetricsValidator()
        self.published_count = 0
        self.last_metrics = None

    def publish(self, metrics: FtmsBridgeMetrics) -> None:
        self.validator.validate(metrics)
        self.transport.send(metrics)
        self.published_count += 1
        self.last_metrics = metrics
