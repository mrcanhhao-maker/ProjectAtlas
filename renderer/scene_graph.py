from dataclasses import dataclass
from typing import Sequence, Tuple


Color = Tuple[int, int, int]


@dataclass(frozen=True)
class SceneNode:
    kind: str
    world_x: float
    world_y: float
    radius: float = 0.0
    width: float = 0.0
    height: float = 0.0
    color: Color = (255, 255, 255)
    label: str = ""
    debug: bool = False


@dataclass(frozen=True)
class SceneGraph:
    nodes: Sequence[SceneNode]
    hud_lines: Sequence[str]
