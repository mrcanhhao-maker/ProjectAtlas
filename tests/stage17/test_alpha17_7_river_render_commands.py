from render_queue import PolygonRenderCommand, RenderCommandQueue


def test_render_queue_stores_polygon_draw_commands():
    command = PolygonRenderCommand(
        layer="river",
        points=(
            (260.0, 0.0),
            (270.0, 100.0),
            (390.0, 100.0),
            (380.0, 0.0),
        ),
    )

    queue = RenderCommandQueue(commands=(command,))

    assert len(queue.commands) == 1
    assert queue.commands[0] == command
