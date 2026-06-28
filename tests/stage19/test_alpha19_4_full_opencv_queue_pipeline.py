import numpy as np

from render_extractor import RenderExtractor
from renderer.opencv_polygon_backend import OpenCvPolygonBackend
from renderer.opencv_queue_renderer import OpenCvQueueRenderer
from river_geometry import RiverCrossSection, RiverGeometryEngine, RiverPath
from scene_graph import RiverSceneNodeFactory, SceneGraph


def test_full_pipeline_draws_river_polygon_into_opencv_frame():
    frame = np.zeros((240, 480, 3), dtype=np.uint8)

    path = RiverPath([
        (240.0, 20.0),
        (240.0, 120.0),
        (240.0, 220.0),
    ])
    section = RiverCrossSection(center_x=240.0, width=120.0)

    geometry = RiverGeometryEngine().build(path, section)
    scene = SceneGraph.empty().add(
        RiverSceneNodeFactory().create(geometry)
    )
    queue = RenderExtractor().extract(scene)

    backend = OpenCvPolygonBackend(
        frame=frame,
        color=(10, 20, 30),
    )
    renderer = OpenCvQueueRenderer(backend)

    renderer.render(queue)

    assert frame[120, 240].tolist() == [10, 20, 30]
    assert frame[120, 50].tolist() == [0, 0, 0]
