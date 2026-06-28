from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.virtual_rower import VirtualRowerEngine


def assert_between(value: float, low: float, high: float, name: str) -> None:
    assert low <= value <= high, f"{name} out of range: {value}"


def test_virtual_rower_engine_active_motion() -> None:
    rower = VirtualRowerEngine()

    state1 = rower.update(
        {
            "stroke_count": 1,
            "spm": 20,
            "quality_score": 0.80,
            "drive_ratio": 0.95,
        },
        timestamp=1000.0,
    )
    state2 = rower.update(
        {
            "stroke_count": 2,
            "spm": 24,
            "quality_score": 0.86,
            "drive_ratio": 1.02,
        },
        timestamp=1001.0,
    )

    assert state1["is_moving"] is True
    assert state2["is_moving"] is True
    assert state2["stroke_count"] == 2
    assert state2["power_watts"] > 0
    assert state2["speed_mps"] > 0
    assert state2["pace_500m"] > 0
    assert state2["distance_m"] > 0
    assert_between(state2["stroke_rate_spm"], 20.0, 30.0, "stroke_rate_spm")


def test_virtual_rower_engine_idle_timeout() -> None:
    rower = VirtualRowerEngine(idle_timeout_s=2.0)

    moving = rower.update(
        {
            "stroke_count": 1,
            "spm": 22,
            "quality_score": 0.8,
            "drive_ratio": 1.0,
        },
        timestamp=2000.0,
    )
    idle = rower.update(
        {
            "stroke_count": 1,
            "spm": 0,
            "quality_score": 0.0,
            "drive_ratio": 0.0,
        },
        timestamp=2003.0,
    )

    assert moving["is_moving"] is True
    assert idle["is_moving"] is False
    assert idle["power_watts"] == 0
    assert idle["speed_mps"] == 0.0


def test_virtual_rower_engine_reset() -> None:
    rower = VirtualRowerEngine()

    rower.update(
        {
            "stroke_count": 3,
            "spm": 25,
            "quality_score": 0.9,
            "drive_ratio": 1.1,
        },
        timestamp=3000.0,
    )
    reset_state = rower.reset()

    assert reset_state.stroke_count == 0
    assert reset_state.power_watts == 0
    assert reset_state.distance_m == 0.0
    assert reset_state.is_moving is False


if __name__ == "__main__":
    test_virtual_rower_engine_active_motion()
    test_virtual_rower_engine_idle_timeout()
    test_virtual_rower_engine_reset()
    print("Alpha12.2 VirtualRowerEngine tests PASS")
