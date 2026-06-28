from engine.ftms_mapper import FtmsMapper, FtmsRowerMeasurement


def test_ftms_mapper_maps_virtual_rower_payload():
    mapper = FtmsMapper()

    result = mapper.map_virtual_rower(
        {
            "elapsed_time_s": 12.5,
            "spm": 28.2,
            "stroke_count": 7,
            "distance_m": 43.8,
            "speed_mps": 3.1,
            "pace_500m_s": 161.3,
            "watts": 185.7,
            "moving": True,
        }
    )

    assert isinstance(result, FtmsRowerMeasurement)
    assert result.elapsed_time_s == 12.5
    assert result.stroke_rate_spm == 28.2
    assert result.stroke_count == 7
    assert result.distance_m == 43.8
    assert result.speed_mps == 3.1
    assert result.pace_500m_s == 161.3
    assert result.power_watts == 186
    assert result.moving is True


def test_ftms_mapper_clamps_invalid_negative_values():
    mapper = FtmsMapper()

    result = mapper.map_virtual_rower(
        {
            "elapsed_time_s": -1,
            "spm": -10,
            "stroke_count": -3,
            "distance_m": -5,
            "speed_mps": -2,
            "pace_500m_s": -100,
            "watts": -50,
            "moving": False,
        }
    )

    assert result.elapsed_time_s == 0.0
    assert result.stroke_rate_spm == 0.0
    assert result.stroke_count == 0
    assert result.distance_m == 0.0
    assert result.speed_mps == 0.0
    assert result.pace_500m_s == 0.0
    assert result.power_watts == 0
    assert result.moving is False


def test_ftms_mapper_infers_moving_from_speed_or_power():
    mapper = FtmsMapper()

    assert mapper.map_virtual_rower({"speed_mps": 0.2}).moving is True
    assert mapper.map_virtual_rower({"watts": 30}).moving is True
    assert mapper.map_virtual_rower({"speed_mps": 0.0, "watts": 0}).moving is False
