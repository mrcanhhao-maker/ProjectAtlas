from dataclasses import dataclass, field
from typing import Sequence

from renderer.world_scene_adapter import BoatSnapshot, WorldRenderSnapshot
from world.boat_state import BoatState


@dataclass(frozen=True)
class RockEntity:
    x: float
    y: float
    radius: float


@dataclass(frozen=True)
class CheckpointEntity:
    x: float
    y: float
    width: float
    label: str


@dataclass(frozen=True)
class CurrentZoneEntity:
    x: float
    y: float
    width: float
    height: float


@dataclass
class PlayableWorld:
    boat: BoatState = field(default_factory=BoatState)
    rocks: Sequence[RockEntity] = field(default_factory=tuple)
    checkpoints: Sequence[CheckpointEntity] = field(default_factory=tuple)
    current_zones: Sequence[CurrentZoneEntity] = field(default_factory=tuple)

    def update(self, dt: float) -> None:
        self.boat.advance(dt)

    def snapshot(self) -> WorldRenderSnapshot:
        return WorldRenderSnapshot(
            boat=BoatSnapshot(x=self.boat.x, y=self.boat.y),
            rocks=tuple(self.rocks),
            checkpoints=tuple(self.checkpoints),
            current_zones=tuple(self.current_zones),
            hud_lines=(
                "ProjectAtlas Alpha 16.5",
                f"Boat y {self.boat.y:.2f} m",
                f"Velocity {self.boat.velocity_mps:.2f} m/s",
            ),
        )
