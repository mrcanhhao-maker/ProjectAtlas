from world.current import CurrentZone
from world.environment import RiverEnvironment
from world.forces import EnvironmentForce
from world.procedural import ProceduralRiverGenerator
from world.vector import Vec2


def test_current_zone_contains_position_inside_bounds():
    zone = CurrentZone(
        zone_id="center-flow",
        center=Vec2(10.0, -100.0),
        width=80.0,
        height=200.0,
        force=EnvironmentForce(forward_acceleration=1.0),
    )

    assert zone.contains(Vec2(10.0, -100.0)) is True
    assert zone.contains(Vec2(49.0, -10.0)) is True
    assert zone.contains(Vec2(80.0, -100.0)) is False


def test_river_environment_builds_three_current_zones_per_chunk():
    environment = RiverEnvironment(
        ProceduralRiverGenerator("atlas-current-zone-test"),
        chunk_height=600.0,
    )

    zones = environment.current_zones_for_chunk(3)

    assert tuple(zone.zone_id for zone in zones) == (
        "chunk:3:current:center",
        "chunk:3:current:left_bank",
        "chunk:3:current:right_bank",
    )


def test_river_environment_force_changes_by_lane_position():
    generator = ProceduralRiverGenerator("atlas-current-force-test")
    environment = RiverEnvironment(generator, chunk_height=600.0)
    spec = generator.chunk_spec(4)

    distance = 4 * 600.0 + 300.0

    center_force = environment.force_at_position(
        lane_x=spec.center_x,
        distance=distance,
    )
    left_force = environment.force_at_position(
        lane_x=spec.center_x - spec.width * 0.38,
        distance=distance,
    )

    assert center_force != left_force
    assert center_force.forward_acceleration > left_force.forward_acceleration
