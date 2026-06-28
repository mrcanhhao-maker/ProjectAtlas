import json

from engine.ftms_bridge_contract import (
    FtmsBridgeMetrics,
    FtmsBridgeMetricsValidator,
)


class FtmsBridgeSerialCodec:
    def __init__(self):
        self.validator = FtmsBridgeMetricsValidator()

    def encode(self, metrics: FtmsBridgeMetrics) -> bytes:
        self.validator.validate(metrics)

        payload = {
            "elapsed_seconds": metrics.elapsed_seconds,
            "stroke_rate_spm": metrics.stroke_rate_spm,
            "stroke_count": metrics.stroke_count,
            "instant_power_watts": metrics.instant_power_watts,
            "total_distance_meters": metrics.total_distance_meters,
            "calories_kcal": metrics.calories_kcal,
        }

        return (json.dumps(payload, separators=(",", ":")) + "\n").encode("utf-8")

    def decode(self, packet: bytes) -> FtmsBridgeMetrics:
        try:
            payload = json.loads(packet.decode("utf-8").strip())
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("invalid bridge metrics packet") from exc

        metrics = FtmsBridgeMetrics(
            elapsed_seconds=int(payload["elapsed_seconds"]),
            stroke_rate_spm=int(payload["stroke_rate_spm"]),
            stroke_count=int(payload["stroke_count"]),
            instant_power_watts=int(payload["instant_power_watts"]),
            total_distance_meters=int(payload["total_distance_meters"]),
            calories_kcal=int(payload["calories_kcal"]),
        )

        self.validator.validate(metrics)
        return metrics
