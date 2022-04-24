"""Contains image selected region model"""
from dataclasses import dataclass
from typing import Generator


@dataclass(frozen=True, kw_only=True)
class ImageSelectedRegion:
    """Dataclass for image selection region"""
    x_1: int
    y_1: int
    x_2: int
    y_2: int

    @property
    def height(self) -> int:
        """Return selected region height"""
        return abs(self.y_2 - self.y_1)

    @property
    def width(self) -> int:
        """Return selected region width"""
        return abs(self.x_2 - self.x_1)

    @property
    def bottom_left_point(self) -> tuple[int, int]:
        """Return left bottom coordinates of the selected region"""
        return min(self.x_1, self.x_2), min(self.y_1, self.y_2)

    @property
    def bottom_right_point(self) -> tuple[int, int]:
        """Return right bottom coordinates of the selected region"""
        return max(self.x_1, self.x_2), min(self.y_1, self.y_2)

    @property
    def top_left_point(self) -> tuple[int, int]:
        """Return left top coordinates of the selected region"""
        return min(self.x_1, self.x_2), max(self.y_1, self.y_2)

    @property
    def attributes_dict(self) -> dict[str, int]:
        """Return dict of rectangle coordinates"""
        return {"x_1": self.x_1, "y_1": self.y_1, "x_2": self.x_2, "y_2": self.y_2}

    @property
    def items(self) -> Generator[tuple[str, int], None, None]:
        """Return generator that returns items of selected rectangle coordinates"""
        for item in self.attributes_dict.items():
            yield item
