from functools import update_wrapper
from typing import Callable, Any, List, Tuple
from datetime import datetime


def print_usage_statistic(function: Callable):
    if not isinstance(function, Spy):
        raise ValueError("Function not decorated with Spy decorator.")
    for value in function.statistics:
        yield value


class Spy:
    def __init__(self, function: Callable) -> None:
        self.statistics: List[Tuple] = []
        self._function = function
        update_wrapper(self, function)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        current_time = str(datetime.now())
        parameters = {"args": args, "kwargs": kwargs}
        self.statistics += [(current_time, parameters)]

        return self._function(*args, **kwargs)
