import pytest

from river_geometry import RiverBanks, RiverPolygonBuilder


def test_river_polygon_builder_combines_left_bank_and_reversed_right_bank():
    banks = RiverBanks(
        left_bank=((260.0, 0.0), (270.0, 100.0), (280.0, 200.0)),
        right_bank=((380.0, 0.0), (390.0, 100.0), (400.0, 200.0)),
    )

    polygon = RiverPolygonBuilder().build(banks)

    assert polygon.points == (
        (260.0, 0.0),
        (270.0, 100.0),
        (280.0, 200.0),
        (400.0, 200.0),
        (390.0, 100.0),
        (380.0, 0.0),
    )


def test_river_polygon_builder_rejects_mismatched_banks():
    banks = RiverBanks(
        left_bank=((260.0, 0.0), (270.0, 100.0)),
        right_bank=((380.0, 0.0),),
    )

    with pytest.raises(ValueError):
        RiverPolygonBuilder().build(banks)
