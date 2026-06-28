from river_geometry import RiverCrossSection, RiverGeometryEngine, RiverPath


def test_river_geometry_engine_builds_complete_geometry_bundle():
    path = RiverPath([
        (320.0, 0.0),
        (330.0, 100.0),
        (340.0, 200.0),
    ])
    section = RiverCrossSection(center_x=320.0, width=120.0)

    geometry = RiverGeometryEngine().build(path, section)

    assert geometry.path is path
    assert geometry.section is section
    assert geometry.banks.left_bank == (
        (260.0, 0.0),
        (270.0, 100.0),
        (280.0, 200.0),
    )
    assert geometry.banks.right_bank == (
        (380.0, 0.0),
        (390.0, 100.0),
        (400.0, 200.0),
    )
    assert geometry.polygon.points == (
        (260.0, 0.0),
        (270.0, 100.0),
        (280.0, 200.0),
        (400.0, 200.0),
        (390.0, 100.0),
        (380.0, 0.0),
    )
    assert geometry.mesh.triangles == (
        (0, 2, 1),
        (1, 2, 3),
        (2, 4, 3),
        (3, 4, 5),
    )
