from pathlib import Path


def test_opencv_queue_renderer_has_no_river_geometry_dependency():
    source = Path("renderer/opencv_queue_renderer.py").read_text()

    assert "river_geometry" not in source
    assert "RiverGeometry" not in source
    assert "RiverPath" not in source
    assert "RiverCrossSection" not in source
    assert "RiverBank" not in source
