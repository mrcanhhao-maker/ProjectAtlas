from world.environment import RiverEnvironment
from world.forces import EnvironmentForce
from world.physics import BoatState, RowingPhysics, StrokeInput
from world.procedural import ProceduralRiverGenerator


def test_environment_force_can_push_boat_forward_without_stroke():
    physics = RowingPhysics()
    state = BoatState(lane_x=0.0, distance=0.0, speed=0.0)

    next_state = physics.step(
        state,
        StrokeInput(stroke_power=0.0, stroke_rate=0.0),
        dt=1.0,
        environment=EnvironmentForce(forward_acceleration=1.2),
    )

    assert next_state.speed == 1.2
    assert next_state.distance == 1.2


def test_environment_force_can_push_boat_laterally():
    physics = RowingPhysics()
    state = BoatState(lane_x=0.0, distance=0.0, speed=0.0)

    next_state = physics.step(
        state,
        StrokeInput(stroke_power=0.0, stroke_rate=0.0),
        dt=2.0,
        environment=EnvironmentForce(lateral_acceleration=0.5),
    )

    assert next_state.lane_x == 1.0


def test_river_environment_is_stable_for_same_seed_and_distance():
    generator = ProceduralRiverGenerator("atlas-flow-test")
    environment = RiverEnvironment(generator, chunk_height=100)

    first = environment.force_at_distance(250)
    second = environment.force_at_distance(250)

    assert first == second
