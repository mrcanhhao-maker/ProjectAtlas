from dataclasses import dataclass


@dataclass(frozen=True)
class RiverCrossSection:
    """
    Production river cross-section contract.

    Coordinates:
    - center_x: river center position on horizontal axis
    - width: full water width from left bank to right bank
    """

    center_x: float
    width: float

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("river cross-section width must be positive")

    @property
    def half_width(self) -> float:
        return self.width / 2.0

    @property
    def left_bank_x(self) -> float:
        return self.center_x - self.half_width

    @property
    def right_bank_x(self) -> float:
        return self.center_x + self.half_width

    def contains_x(self, x: float) -> bool:
        return self.left_bank_x <= x <= self.right_bank_x
