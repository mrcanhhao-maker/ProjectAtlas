import pytest

from river_geometry import RiverBanks, RiverMeshBuilder


def test_river_mesh_builder_interleaves_left_and_right_bank_vertices():
    banks = RiverBanks(
        left_bank=((260.0, 0.0), (270.0, 100.0), (280.0, 200.0)),
        right_bank=((380.0, 0.0), (390.0, 100.0), (400.0, 200.0)),
    )

    mesh = RiverMeshBuilder().build(banks)

    assert mesh.vertices == (
        (260.0, 0.0),
        (380.0, 0.0),
        (270.0, 100.0),
        (390.0, 100.0),
        (280.0, 200.0),
        (400.0, 200.0),
    )
    assert mesh.triangles == (
        (0, 2, 1),
        (1, 2, 3),
        (2, 4, 3),
        (3, 4, 5),
    )


def test_river_mesh_builder_rejects_mismatched_banks():
    banks = RiverBanks(
        left_bank=((260.0, 0.0), (270.0, 100.0)),
        right_bank=((380.0, 0.0),),
    )

    with pytest.raises(ValueError):
        RiverMeshBuilder().build(banks)
