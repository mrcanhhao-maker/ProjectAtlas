import pytest

from river_geometry import RiverPath


def test_river_path_requires_two_points():
    with pytest.raises(ValueError):
        RiverPath([(0.0, 0.0)])


def test_river_path_properties():
    path = RiverPath([
        (320.0, 0.0),
        (325.0, 100.0),
        (330.0, 200.0),
    ])

    assert path.segments == 2
    assert path.start == (320.0, 0.0)
    assert path.end == (330.0, 200.0)
