from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from atlas_platform.core_runtime import CoreRuntime
from atlas_platform.dev_playable_loop import DevPlayableLoop
from atlas_platform.opencv_display_runtime import OpenCVDisplayRuntime
from renderer.opencv_world_renderer import OpenCVWorldRenderer, RenderConfig
from renderer.render_extractor import RenderExtractor
from renderer.world_scene_adapter import WorldSceneAdapter
from world.boat_state import BoatState
from world.playable_world import CheckpointEntity, CurrentZoneEntity, PlayableWorld, RockEntity


def build_world() -> PlayableWorld:
    rocks = tuple(
        RockEntity(x=x, y=y, radius=r)
        for x, y, r in [
            (-8, 116, 1.1),
            (7, 128, 1.4),
            (-3, 144, 1.0),
            (9, 165, 1.6),
            (-7, 188, 1.3),
            (4, 215, 1.0),
            (-10, 242, 1.5),
        ]
    )

    checkpoints = (
        CheckpointEntity(x=0, y=150, width=22, label="CP1"),
        CheckpointEntity(x=0, y=260, width=22, label="CP2"),
        CheckpointEntity(x=0, y=380, width=22, label="CP3"),
    )

    current_zones = (
        CurrentZoneEntity(x=-4, y=132, width=14, height=18),
        CurrentZoneEntity(x=5, y=222, width=16, height=24),
        CurrentZoneEntity(x=0, y=330, width=22, height=28),
    )

    return PlayableWorld(
        boat=BoatState(x=0.0, y=100.0, velocity_mps=8.0),
        rocks=rocks,
        checkpoints=checkpoints,
        current_zones=current_zones,
    )


def main() -> None:
    world = build_world()
    runtime = CoreRuntime(
        world=world,
        scene_adapter=WorldSceneAdapter(),
        render_extractor=RenderExtractor(),
    )
    display = OpenCVDisplayRuntime(
        renderer=OpenCVWorldRenderer(
            RenderConfig(width=1280, height=720, pixels_per_meter=18.0)
        ),
        window_name="ProjectAtlas Alpha 16.5 - Dev Playable River",
    )

    DevPlayableLoop(runtime=runtime, display=display, target_fps=60).run()


if __name__ == "__main__":
    main()
