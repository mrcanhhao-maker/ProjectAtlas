from dataclasses import dataclass


@dataclass(frozen=True)
class FtmsBridgeMetrics:
    elapsed_seconds: int
    stroke_rate_spm: int
    stroke_count: int
    instant_power_watts: int
    total_distance_meters: int
    calories_kcal: int


class FtmsBridgeMetricsValidator:
    def validate(self, metrics: FtmsBridgeMetrics) -> None:
        if metrics.elapsed_seconds < 0:
            raise ValueError("elapsed_seconds must be >= 0")

        if not 0 <= metrics.stroke_rate_spm <= 120:
            raise ValueError("stroke_rate_spm must be between 0 and 120")

        if metrics.stroke_count < 0:
            raise ValueError("stroke_count must be >= 0")

        if not 0 <= metrics.instant_power_watts <= 2000:
            raise ValueError("instant_power_watts must be between 0 and 2000")

        if metrics.total_distance_meters < 0:
            raise ValueError("total_distance_meters must be >= 0")

        if metrics.calories_kcal < 0:
            raise ValueError("calories_kcal must be >= 0")
