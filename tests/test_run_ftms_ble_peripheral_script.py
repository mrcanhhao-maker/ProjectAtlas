from pathlib import Path


def test_run_ftms_ble_peripheral_script_is_import_safe():
    script = Path("scripts/run_ftms_ble_peripheral.py").read_text()

    assert "PROJECT_ROOT = Path(__file__).resolve().parents[1]" in script
    assert "sys.path.insert(0, str(PROJECT_ROOT))" in script
    assert "FtmsBlePeripheralController" in script
    assert 'local_name="ProjectAtlas-FTMS"' in script
    assert "controller.stop()" in script
