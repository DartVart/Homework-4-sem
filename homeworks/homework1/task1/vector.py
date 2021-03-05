from math import sqrt, acos
from typing import List


class Vector:
    __values: List[float]

    def __init__(self, *values: float) -> None:
        if not values:
            raise ValueError("No values passed to define a vector.")

        self.__values = list(values)

    def dot(self, other: "Vector") -> float:
        if len(other.__values) != len(self.__values):
            raise ValueError("The dimensions of the vectors don't match.")

        return sum(x * y for x, y in zip(self.__values, other.__values))

    def norm(self) -> float:
        return sqrt(self.dot(self))

    def angle(self, other: "Vector") -> float:
        """Returns the angle in radians"""
        if self.norm() == 0 or other.norm() == 0:
            raise ZeroDivisionError("Can't find angle between zero vector and some other.")

        return acos(self.dot(other) / (self.norm() * other.norm()))
