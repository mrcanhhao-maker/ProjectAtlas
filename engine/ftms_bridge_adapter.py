from engine.ftms_bridge_contract import FtmsBridgeMetrics


class FtmsBridgeMetricsAdapter:
    def from_runtime_rower_state(self, state: dict) -> FtmsBridgeMetrics:
        return FtmsBridgeMetrics(
            elapsed_seconds=self._int_value(state, "elapsed_seconds"),
            stroke_rate_spm=self._int_value(state, "spm"),
            stroke_count=self._int_value(state, "stroke_count"),
            instant_power_watts=self._int_value(state, "power"),
            total_distance_meters=self._int_value(state, "distance"),
            calories_kcal=self._int_value(state, "calories"),
        )

    def _int_value(self, state: dict, key: str) -> int:
        if key not in state:
            raise KeyError(f"missing rower state field: {key}")

        value = state[key]

        if value is None:
            raise ValueError(f"rower state field is None: {key}")

        return int(round(float(value)))
