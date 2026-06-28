from dataclasses import dataclass
from typing import Iterable, Tuple

from renderer.render_command import RenderCommand


@dataclass(frozen=True)
class RenderQueue:
    commands: Tuple[RenderCommand, ...]

    @classmethod
    def from_commands(cls, commands: Iterable[RenderCommand]) -> "RenderQueue":
        return cls(commands=tuple(sorted(commands, key=lambda command: command.layer)))
