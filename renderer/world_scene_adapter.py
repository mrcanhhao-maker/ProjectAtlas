from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from renderer.scene_graph import SceneGraph, SceneNode


@dataclass(frozen=True)
class BoatSnapshot:
    x: float
    y: float


@dataclass(frozen=True)
class WorldRenderSnapshot:
    boat: BoatSnapshot
    rocks: Sequence[Any]
    checkpoints: Sequence[Any]
    current_zones: Sequence[Any]
    hud_lines: Sequence[str]


class WorldSceneAdapter:
    def build_scene(self, snapshot: WorldRenderSnapshot) -> SceneGraph:
        nodes: list[SceneNode] = []

        for rock in snapshot.rocks:
            nodes.append(
                SceneNode(
                    kind="rock",
                    world_x=float(getattr(rock, "x")),
                    world_y=float(getattr(rock, "y")),
                    radius=float(getattr(rock, "radius", 1.0)),
                    color=(82, 82, 82),
                )
            )

        for checkpoint in snapshot.checkpoints:
            nodes.append(
                SceneNode(
                    kind="checkpoint",
                    world_x=float(getattr(checkpoint, "x")),
                    world_y=float(getattr(checkpoint, "y")),
                    width=float(getattr(checkpoint, "width", 10.0)),
                    color=(0, 220, 255),
                    label=str(getattr(checkpoint, "label", "")),
                )
            )

        for zone in snapshot.current_zones:
            nodes.append(
                SceneNode(
                    kind="current_zone",
                    world_x=float(getattr(zone, "x")),
                    world_y=float(getattr(zone, "y")),
                    width=float(getattr(zone, "width", 10.0)),
                    height=float(getattr(zone, "height", 8.0)),
                    color=(255, 160, 0),
                    debug=True,
                )
            )

        return SceneGraph(nodes=tuple(nodes), hud_lines=tuple(snapshot.hud_lines))
