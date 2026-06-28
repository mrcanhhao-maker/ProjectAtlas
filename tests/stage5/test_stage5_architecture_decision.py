from pathlib import Path


def test_stage5_architecture_decision_documents_corebluetooth_blocker():
    doc = Path("docs/stage5_ftms_architecture_decision.md").read_text()

    assert "LightBlue on iPhone does not discover ProjectAtlas FTMS GATT" in doc
    assert "Do not continue FTMS notify/read/write callbacks" in doc
    assert "FTMS service 1826" in doc


def test_stage5_architecture_decision_preserves_vision_engine():
    doc = Path("docs/stage5_ftms_architecture_decision.md").read_text()

    assert "Do not replace Vision Engine" in doc
    assert "MacBook:" in doc
    assert "ESP32:" in doc
