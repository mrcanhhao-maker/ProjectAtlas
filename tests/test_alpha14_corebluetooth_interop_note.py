from pathlib import Path


def test_alpha14_corebluetooth_interop_note_records_current_blocker():
    note = Path("docs/alpha14_corebluetooth_interop.md").read_text()

    assert "0x1826" in note
    assert "0x2AD1" in note
    assert "0x2ACC" in note
    assert "0x2ADA" in note
    assert "LightBlue" in note
    assert "Apple Inc." in note
    assert "Do not continue adding FTMS notify/read/write callbacks" in note
