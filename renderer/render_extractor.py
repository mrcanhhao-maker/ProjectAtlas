from renderer.render_command import RenderCommand
from renderer.render_queue import RenderQueue
from renderer.scene_graph import SceneGraph


class RenderExtractor:
    def extract(self, scene: SceneGraph) -> RenderQueue:
        commands: list[RenderCommand] = []

        for node in scene.nodes:
            if node.kind == "current_zone":
                commands.append(
                    RenderCommand(
                        layer=10,
                        kind="rect",
                        color=node.color,
                        world_x=node.world_x,
                        world_y=node.world_y,
                        width=node.width,
                        height=node.height,
                        alpha=0.25,
                    )
                )
            elif node.kind == "rock":
                commands.append(
                    RenderCommand(
                        layer=30,
                        kind="circle",
                        color=node.color,
                        world_x=node.world_x,
                        world_y=node.world_y,
                        radius=node.radius,
                    )
                )
            elif node.kind == "checkpoint":
                half_width = node.width * 0.5
                commands.append(
                    RenderCommand(
                        layer=20,
                        kind="line",
                        color=node.color,
                        points=(
                            (node.world_x - half_width, node.world_y),
                            (node.world_x + half_width, node.world_y),
                        ),
                        thickness=3,
                    )
                )
                if node.label:
                    commands.append(
                        RenderCommand(
                            layer=21,
                            kind="text",
                            color=node.color,
                            world_x=node.world_x - half_width,
                            world_y=node.world_y - 0.6,
                            text=node.label,
                            font_scale=0.55,
                            thickness=2,
                        )
                    )

        hud_y = 1.0
        for line in scene.hud_lines[:6]:
            commands.append(
                RenderCommand(
                    layer=1000,
                    kind="text",
                    color=(245, 245, 245),
                    world_x=1.3,
                    world_y=hud_y,
                    text=line,
                    font_scale=0.72,
                    thickness=2,
                )
            )
            hud_y += 1.1

        return RenderQueue.from_commands(commands)
