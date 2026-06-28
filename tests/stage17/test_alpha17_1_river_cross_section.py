import pytest

from river_geometry import RiverCrossSection


def test_river_cross_section_exposes_bank_positions():
    section = RiverCrossSection(center_x=320.0, width=160.0)

    assert section.half_width == 80.0
    assert section.left_bank_x == 240.0
    assert section.right_bank_x == 400.0


def test_river_cross_section_contains_x_inside_water():
    section = RiverCrossSection(center_x=320.0, width=160.0)

    assert section.contains_x(240.0)
    assert section.contains_x(320.0)
    assert section.contains_x(400.0)


def test_river_cross_section_rejects_non_positive_width():
    with pytest.raises(ValueError):
        RiverCrossSection(center_x=320.0, width=0.0)

    with pytest.raises(ValueError):
        RiverCrossSection(center_x=320.0, width=-1.0)
