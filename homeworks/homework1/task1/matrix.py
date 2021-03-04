from typing import List, Tuple

from homeworks.homework1.task1.vector import Vector


class Matrix:
    __values: List[List[float]]
    __equality_delta: float
    size: Tuple[int, int]

    def __init__(self, *values: List[float], equality_delta: float = 0.0001) -> None:
        """
        :param equality_delta: Required for comparing tables.
            Tables will be equal if their sizes are the same and
            the difference in values in the corresponding cells
            doesn't exceed the equality_delta.
        """
        if not values or not values[0]:
            raise ValueError("No values passed to define a matrix.")

        first_row_length = len(values[0])

        if any(len(row) != first_row_length for row in values):
            raise ValueError("Rows in the matrix must be the same length.")

        self.size = (len(values), first_row_length)
        self.__equality_delta = equality_delta
        self.__values = list(values)

    def __eq__(self, other):
        return isinstance(other, Matrix) and all(
            [
                abs(x - y) <= self.__equality_delta for x, y in zip(row_1, row_2)
            ]
            for row_1, row_2 in zip(self.__values, other.__values)
        )

    def __add__(self, other: "Matrix") -> "Matrix":
        if self.size != other.size:
            raise ValueError("Matrix sizes aren't suitable for addition.")

        return Matrix(*[[x + y for x, y in zip(row_1, row_2)] for row_1, row_2 in zip(self.__values, other.__values)])

    def transpose(self) -> "Matrix":
        return Matrix(*[list(column) for column in zip(*self.__values)])

    def __mul__(self, other: "Matrix") -> "Matrix":
        if self.size[1] != other.size[0]:
            raise ValueError("Matrix sizes aren't suitable for multiplication.")
        return Matrix(
            *[
                [
                    Vector(*row).dot(Vector(*column)) for column in other.transpose().__values
                ]
                for row in self.__values
            ]
        )
