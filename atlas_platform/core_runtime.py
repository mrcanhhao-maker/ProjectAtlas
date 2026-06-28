from dataclasses import dataclass
from time import perf_counter

from atlas_platform.runtime_contract import RuntimeFrame
from renderer.render_extractor import RenderExtractor
from renderer.world_scene_adapter import WorldSceneAdapter
from world.playable_world import PlayableWorld


@dataclass
class CoreRuntime:
    world: PlayableWorld
    scene_adapter: WorldSceneAdapter
    render_extractor: RenderExtractor
    _last_time: float | None = None
    _fps: float = 0.0

    def update(self, dt: float) -> RuntimeFrame:
        if dt < 0:
            raise ValueError("dt must be non-negative")

        self.world.update(dt)
        snapshot = self.world.snapshot()
        scene = self.scene_adapter.build_scene(snapshot)
        queue = self.render_extractor.extract(scene)

        now = perf_counter()
        if self._last_time is not None:
            elapsed = now - self._last_time
            if elapsed > 0:
                self._fps = 1.0 / elapsed
        self._last_time = now

        return RuntimeFrame(
            render_queue=queue,
            boat_x=snapshot.boat.x,
            boat_y=snapshot.boat.y,
            fps=self._fps,
        )
