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
    def _world_x(self, obj: Any) -> float:
        if hasattr(obj, "x"):
            return float(getattr(obj, "x"))
        position = getattr(obj, "position")
        return float(getattr(position, "x"))

    def _world_y(self, obj: Any) -> float:
        if hasattr(obj, "y"):
            return float(getattr(obj, "y"))
        position = getattr(obj, "position")
        return float(getattr(position, "y"))

    def build_scene(self, snapshot: WorldRenderSnapshot) -> SceneGraph:
        nodes: list[SceneNode] = []

        for rock in snapshot.rocks:
            nodes.append(
                SceneNode(
                    kind="rock",
                    world_x=self._world_x(rock),
                    world_y=self._world_y(rock),
                    radius=float(getattr(rock, "radius", 1.0)),
                    color=(82, 82, 82),
                )
            )

        for checkpoint in snapshot.checkpoints:
            nodes.append(
                SceneNode(
                    kind="checkpoint",
                    world_x=self._world_x(checkpoint),
                    world_y=self._world_y(checkpoint),
                    width=float(getattr(checkpoint, "width", 10.0)),
                    color=(0, 220, 255),
                    label=str(getattr(checkpoint, "label", "")),
                )
            )

        for zone in snapshot.current_zones:
            nodes.append(
                SceneNode(
                    kind="current_zone",
                    world_x=self._world_x(zone),
                    world_y=self._world_y(zone),
                    width=float(getattr(zone, "width", 10.0)),
                    height=float(getattr(zone, "height", 8.0)),
                    color=(255, 160, 0),
                    debug=True,
                )
            )

        return SceneGraph(nodes=tuple(nodes), hud_lines=tuple(snapshot.hud_lines))
