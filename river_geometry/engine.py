from dataclasses import dataclass

from .banks import RiverBankGenerator, RiverBanks
from .cross_section import RiverCrossSection
from .mesh import RiverMesh, RiverMeshBuilder
from .path import RiverPath
from .polygon import RiverPolygon, RiverPolygonBuilder


@dataclass(frozen=True)
class RiverGeometry:
    path: RiverPath
    section: RiverCrossSection
    banks: RiverBanks
    polygon: RiverPolygon
    mesh: RiverMesh


class RiverGeometryEngine:
    """
    Production river geometry pipeline.

    Renderer-independent:
    - no OpenCV
    - no camera logic
    - no boat logic
    - no color/style decision
    """

    def __init__(self) -> None:
        self._bank_generator = RiverBankGenerator()
        self._polygon_builder = RiverPolygonBuilder()
        self._mesh_builder = RiverMeshBuilder()

    def build(self, path: RiverPath, section: RiverCrossSection) -> RiverGeometry:
        banks = self._bank_generator.generate(path, section)
        polygon = self._polygon_builder.build(banks)
        mesh = self._mesh_builder.build(banks)

        return RiverGeometry(
            path=path,
            section=section,
            banks=banks,
            polygon=polygon,
            mesh=mesh,
        )
