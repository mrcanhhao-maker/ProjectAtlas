from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class SceneNode:
    node_type: str
    payload: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not self.node_type:
            raise ValueError("scene node type must not be empty")


@dataclass(frozen=True)
class SceneGraph:
    nodes: tuple[SceneNode, ...]

    @classmethod
    def empty(cls) -> "SceneGraph":
        return cls(nodes=())

    def add(self, node: SceneNode) -> "SceneGraph":
        return SceneGraph(nodes=self.nodes + (node,))
