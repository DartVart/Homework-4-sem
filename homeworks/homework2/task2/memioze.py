from functools import update_wrapper
from typing import Callable, OrderedDict as OrderedDictType, Optional, Tuple, Dict, Any
from collections import OrderedDict


def memoize(function: Optional[Callable] = None, *, size: int = 0) -> Callable:
    """
    Decorator that allows you to cache function values.

    :param function: function for caching
    :param size: maximum size of stored function results
    :return: cached function
    """
    if size < 0:
        raise ValueError("Cache size cannot be negative.")

    if function is None:
        return lambda func: FunctionMemoizer(func, size=size)

    return FunctionMemoizer(function, size=size)


class FunctionMemoizer:
    _function: Callable
    _size: int
    _cache: OrderedDictType

    def __init__(self, function=None, *, size: int = 0):
        if size < 0:
            raise ValueError("The size cannot be negative.")

        self._size = size
        self._cache = OrderedDict()
        self._function = function
        update_wrapper(self, function)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._size == 0:
            return self._function(*args, **kwargs)

        key = self.__get_key(args, kwargs)
        if key in self._cache:
            return self._cache[key]

        new_result = self._function(*args, **kwargs)
        if len(self._cache) >= self._size:
            self._cache.popitem(last=False)

        self._cache[key] = new_result

        return new_result

    @staticmethod
    def __get_key(func_args: Tuple, func_kwargs: Dict[str, Any]) -> Tuple:
        return func_args + tuple(sorted(func_kwargs.items()))
