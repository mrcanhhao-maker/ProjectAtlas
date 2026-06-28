from render_queue import RenderCommandQueue
from river_geometry import RiverPolygon


def test_render_queue_converts_river_polygon_to_draw_command():
    polygon = RiverPolygon(points=(
        (260.0, 0.0),
        (270.0, 100.0),
        (390.0, 100.0),
        (380.0, 0.0),
    ))

    queue = RenderCommandQueue.from_river_polygon(polygon)

    assert len(queue.commands) == 1
    assert queue.commands[0].layer == "river"
    assert queue.commands[0].points == polygon.points
