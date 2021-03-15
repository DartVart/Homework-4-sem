from copy import deepcopy
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar("T")


class SmartArgument(Generic[T]):
    """Parent class for all smart arguments"""

    def get_new_argument(self, current_arg: Optional[T]) -> T:
        """
        Returns the processed argument

        :param current_arg: the argument that was passed in for processing. It may be None
        :return: a new argument of the same type as passed
        """
        ...


class Isolated(SmartArgument[T]):
    """A smart argument deeply copying the current argument"""

    def get_new_argument(self, current_arg: Optional[T]) -> T:
        if current_arg is None:
            raise ValueError("Argument using Isolated has not been assigned a value.")
        return deepcopy(current_arg)


class Evaluated(SmartArgument[T]):
    def __init__(self, function: Callable[[], T]):
        """
        A smart argument that calls a function
        that returns a new argument if the current argument is None.
        Otherwise, the current argument is returned.

        :param function: function that returns new arguments
        """
        if isinstance(function, Isolated) or function is Isolated:
            raise ValueError("Can't use Evaluated with Isolated.")

        self.__function = function

    def get_new_argument(self, current_arg: Optional[T]) -> T:
        if current_arg is None:
            return self.__function()
        return current_arg
