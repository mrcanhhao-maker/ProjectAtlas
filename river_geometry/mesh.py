from dataclasses import dataclass
from typing import Tuple

from .banks import RiverBanks


Point = Tuple[float, float]
Triangle = Tuple[int, int, int]


@dataclass(frozen=True)
class RiverMesh:
    vertices: tuple[Point, ...]
    triangles: tuple[Triangle, ...]

    def __post_init__(self) -> None:
        if len(self.vertices) < 4:
            raise ValueError("river mesh requires at least four vertices")
        if not self.triangles:
            raise ValueError("river mesh requires at least one triangle")


class RiverMeshBuilder:
    """
    Builds a triangle-strip style mesh from generated banks.

    This is renderer-independent geometry data.
    """

    def build(self, banks: RiverBanks) -> RiverMesh:
        if len(banks.left_bank) != len(banks.right_bank):
            raise ValueError("left and right river banks must have the same sample count")
        if len(banks.left_bank) < 2:
            raise ValueError("river mesh requires at least two samples per bank")

        vertices = tuple(
            point
            for pair in zip(banks.left_bank, banks.right_bank)
            for point in pair
        )

        triangles = []
        for sample_index in range(len(banks.left_bank) - 1):
            left_a = sample_index * 2
            right_a = left_a + 1
            left_b = left_a + 2
            right_b = left_a + 3

            triangles.append((left_a, left_b, right_a))
            triangles.append((right_a, left_b, right_b))

        return RiverMesh(vertices=vertices, triangles=tuple(triangles))
