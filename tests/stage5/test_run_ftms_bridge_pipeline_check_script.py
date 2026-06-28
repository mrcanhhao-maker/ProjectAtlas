from pathlib import Path


def test_run_ftms_bridge_pipeline_check_script_exists_and_uses_pipeline():
    script = Path("scripts/run_ftms_bridge_pipeline_check.py").read_text()

    assert "FtmsBridgePipeline" in script
    assert "publish_runtime_rower_state" in script
    assert "InMemoryFtmsBridgeTransport" in script
