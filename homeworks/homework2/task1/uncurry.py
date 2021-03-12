from typing import Any, Callable


def uncurry_explicit(function: Callable, arity: int) -> Callable:
    """
    Converts a sequence of functions that each take a single argument into a function that takes multiple arguments

    :param function: curried function
    :param arity: the number of arguments the function takes
    :return uncurried function:
    """
    if arity == 0:
        return function
    if arity < 0:
        raise ValueError("Arity cannot be negative.")

    def inner(*args: Any) -> Callable:
        if len(args) != arity:
            raise TypeError("Arity doesn't match the number of arguments.")

        result = function
        for argument in args:
            result = result(argument)
        return result

    return inner
