from typing import Callable, Any


def curry_explicit(function: Callable, arity: int) -> Callable:
    """
    Converts a function that takes multiple arguments into a sequence of functions that each take a single argument

    :param function: function for currying
    :param arity: the number of arguments the function takes
    :return curried function:
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative.")

    def inner(*args: Any) -> Callable:
        if len(args) > arity:
            raise TypeError("Number of arguments doesn't match arity.")

        if len(args) == arity:
            return function(*args)

        return lambda x: inner(*args, x)

    return inner
