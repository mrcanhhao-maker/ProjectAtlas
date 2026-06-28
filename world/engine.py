from dataclasses import dataclass

from world.camera import TopDownRiverCamera
from world.collision import CollisionEngine, CollisionReport
from world.culling import ViewportCuller
from world.environment import RiverEnvironment
from world.hud import RiverHud
from world.mission import RiverMission
from world.physics import BoatState, RowingPhysics, StrokeInput
from world.objects import WorldObject
from world.renderer import RenderFrame, RiverRenderer
from world.procedural import ProceduralRiverGenerator
from world.river_map import RiverMap
from world.streaming import RiverChunkGenerator, RiverStream
from world.viewport import ViewportFactory


@dataclass(frozen=True)
class WorldEngineSnapshot:
    boat: BoatState
    frame: RenderFrame
    collision: CollisionReport


class RiverWorldEngine:
    def __init__(self, river_map: RiverMap) -> None:
        self.river_map = river_map
        self.physics = RowingPhysics()
        self.procedural = ProceduralRiverGenerator(seed="atlas-alpha15")
        self.environment = RiverEnvironment(self.procedural)
        self.camera = TopDownRiverCamera()
        self.mission = RiverMission(river_map)
        self.hud = RiverHud()
        self.renderer = RiverRenderer()
        self.viewport_factory = ViewportFactory()
        self.culler = ViewportCuller()
        self.collision_engine = CollisionEngine()
        self.static_world_objects = self._build_world_objects(river_map)
        self.river_stream = RiverStream(
            generator=RiverChunkGenerator(procedural=self.procedural)
        )
        self.boat = BoatState(lane_x=0.0, distance=0.0, speed=0.0)

    def step(self, stroke: StrokeInput, dt: float) -> WorldEngineSnapshot:
        environment_force = self.environment.force_at_distance(self.boat.distance)
        self.boat = self.physics.step(self.boat, stroke, dt, environment_force)
        camera_state = self.camera.follow(self.boat)
        mission_state = self.mission.evaluate(self.boat)
        hud_snapshot = self.hud.build(self.boat, mission_state)
        viewport = self.viewport_factory.from_camera(camera_state)
        streamed_objects = self.river_stream.update(viewport)
        world_objects = self.static_world_objects + streamed_objects
        visible_objects = self.culler.visible_objects(world_objects, viewport)
        collision_report = self.collision_engine.detect(self.boat, world_objects)
        frame = self.renderer.build_frame(self.river_map, camera_state, hud_snapshot, visible_objects)
        return WorldEngineSnapshot(boat=self.boat, frame=frame, collision=collision_report)


    def _build_world_objects(self, river_map: RiverMap) -> tuple[WorldObject, ...]:
        objects = []

        for index, waypoint in enumerate(river_map.waypoints):
            objects.append(
                WorldObject(
                    object_id=f"waypoint:{index}",
                    kind="river_waypoint",
                    position=waypoint.position,
                    radius=waypoint.width / 2,
                )
            )

        for index, obstacle in enumerate(river_map.obstacles):
            objects.append(
                WorldObject(
                    object_id=f"obstacle:{index}:{obstacle.kind}",
                    kind=obstacle.kind,
                    position=obstacle.position,
                    radius=obstacle.radius,
                )
            )

        for checkpoint in river_map.checkpoints:
            objects.append(
                WorldObject(
                    object_id=f"checkpoint:{checkpoint.name}",
                    kind="checkpoint",
                    position=checkpoint.position,
                    radius=32.0,
                )
            )

        return tuple(objects)
