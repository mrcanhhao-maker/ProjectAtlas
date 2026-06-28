from render_queue import PolygonRenderCommand, RenderCommandQueue
from scene_graph import SceneGraph


class RenderExtractor:
    """
    Converts renderer-independent SceneGraph into RenderCommandQueue.

    Renderer backends consume only commands.
    """

    def extract(self, scene: SceneGraph) -> RenderCommandQueue:
        commands = []

        for node in scene.nodes:
            if node.node_type == "river":
                commands.append(
                    PolygonRenderCommand(
                        layer="river",
                        points=tuple(node.payload["polygon_points"]),
                    )
                )

        return RenderCommandQueue(commands=tuple(commands))
