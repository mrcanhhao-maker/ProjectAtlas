from pathlib import Path


def test_stage6_2_research_records_mywhoosh_ftms_advertising_blocker():
    doc = Path("docs/stage6_2_mywhoosh_ftms_research.md").read_text()

    assert "MyWhoosh version 5.8.0 supports FTMS-compatible rowing machines" in doc
    assert "advertisement-level filtering" in doc
    assert "Fitness Machine Service UUID: 0x1826" in doc
    assert "Fitness Machine Type bit 4: Rower Supported" in doc
    assert "CBAdvertisementDataLocalNameKey" in doc
    assert "CBAdvertisementDataServiceUUIDsKey" in doc
    assert "cannot fully advertise FTMS Service Data" in doc
    assert "Do not use ESP32" in doc
