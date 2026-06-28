import numpy as np

from render_extractor import RenderExtractor
from renderer.opencv_polygon_backend import OpenCvPolygonBackend
from renderer.opencv_queue_renderer import OpenCvQueueRenderer
from river_geometry import RiverCrossSection, RiverGeometryEngine, RiverPath
from scene_graph import RiverSceneNodeFactory, SceneGraph


def test_opencv_backend_contract_uses_queue_only_for_river_rendering():
    frame = np.zeros((300, 500, 3), dtype=np.uint8)

    geometry = RiverGeometryEngine().build(
        RiverPath([
            (250.0, 20.0),
            (250.0, 150.0),
            (250.0, 280.0),
        ]),
        RiverCrossSection(center_x=250.0, width=160.0),
    )

    scene = SceneGraph.empty().add(
        RiverSceneNodeFactory().create(geometry)
    )
    queue = RenderExtractor().extract(scene)

    backend = OpenCvPolygonBackend(frame=frame, color=(7, 8, 9))
    renderer = OpenCvQueueRenderer(backend)

    renderer.render(queue)

    assert frame[150, 250].tolist() == [7, 8, 9]
    assert frame[150, 50].tolist() == [0, 0, 0]
