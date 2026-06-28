from dataclasses import dataclass
from typing import Tuple

from .cross_section import RiverCrossSection
from .path import RiverPath


Point = Tuple[float, float]


@dataclass(frozen=True)
class RiverBanks:
    left_bank: tuple[Point, ...]
    right_bank: tuple[Point, ...]


class RiverBankGenerator:
    """
    Generates river banks from center-line samples.

    Alpha 17.3 keeps width constant by cross-section contract.
    Curved perpendicular offsets will come later.
    """

    def generate(self, path: RiverPath, section: RiverCrossSection) -> RiverBanks:
        left = tuple((x - section.half_width, y) for x, y in path.points)
        right = tuple((x + section.half_width, y) for x, y in path.points)

        return RiverBanks(left_bank=left, right_bank=right)
