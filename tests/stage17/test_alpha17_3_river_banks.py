from river_geometry import RiverBankGenerator, RiverCrossSection, RiverPath


def test_river_bank_generator_offsets_path_by_half_width():
    path = RiverPath([
        (320.0, 0.0),
        (330.0, 100.0),
        (340.0, 200.0),
    ])
    section = RiverCrossSection(center_x=320.0, width=120.0)

    banks = RiverBankGenerator().generate(path, section)

    assert banks.left_bank == (
        (260.0, 0.0),
        (270.0, 100.0),
        (280.0, 200.0),
    )
    assert banks.right_bank == (
        (380.0, 0.0),
        (390.0, 100.0),
        (400.0, 200.0),
    )


def test_river_bank_generator_preserves_sample_count():
    path = RiverPath([
        (320.0, 0.0),
        (325.0, 100.0),
    ])
    section = RiverCrossSection(center_x=320.0, width=100.0)

    banks = RiverBankGenerator().generate(path, section)

    assert len(banks.left_bank) == len(path.points)
    assert len(banks.right_bank) == len(path.points)
