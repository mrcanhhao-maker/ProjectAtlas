from pathlib import Path


def test_lightblue_discovery_update_records_ftms_service_and_characteristics():
    doc = Path("docs/stage5_lightblue_ftms_discovery.md").read_text()

    assert "00001826-0000-1000-8000-00805F9B34FB" in doc
    assert "00002AD1-0000-1000-8000-00805F9B34FB" in doc
    assert "00002ACC-0000-1000-8000-00805F9B34FB" in doc
    assert "00002ADA-0000-1000-8000-00805F9B34FB" in doc


def test_lightblue_discovery_update_keeps_laptop_only_path_open():
    doc = Path("docs/stage5_lightblue_ftms_discovery.md").read_text()

    assert "Do not move to ESP32 yet" in doc
    assert "Continue laptop-only CoreBluetooth path" in doc
    assert "Confirm central subscription to 2AD1" in doc
