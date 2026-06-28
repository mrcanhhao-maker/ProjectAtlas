from pathlib import Path


def test_stage5_lightblue_notify_validation_documented():
    doc = Path("docs/stage5_lightblue_notify_validation.md").read_text()

    assert "00001826-0000-1000-8000-00805F9B34FB" in doc
    assert "00002AD1-0000-1000-8000-00805F9B34FB" in doc
    assert "notify values are received continuously" in doc
    assert "LightBlue FTMS discovery, subscription, and notification validation passed" in doc
    assert "MyWhoosh" in doc
