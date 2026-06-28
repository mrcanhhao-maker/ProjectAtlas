from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from engine.ftms_bridge_contract import FtmsBridgeMetrics
from engine.ftms_bridge_serial import FtmsBridgeSerialCodec


class FtmsBridgeTransport(ABC):
    @abstractmethod
    def send(self, metrics: FtmsBridgeMetrics) -> None:
        raise NotImplementedError


@dataclass
class InMemoryFtmsBridgeTransport(FtmsBridgeTransport):
    packets: List[bytes]

    def __post_init__(self):
        self.codec = FtmsBridgeSerialCodec()

    def send(self, metrics: FtmsBridgeMetrics) -> None:
        self.packets.append(self.codec.encode(metrics))
