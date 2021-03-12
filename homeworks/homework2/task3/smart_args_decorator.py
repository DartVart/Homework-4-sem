import inspect
from functools import update_wrapper
from typing import Any, Optional, Callable, Dict, List

from homeworks.homework2.task3.smart_args import Isolated, Evaluated, SmartArgument


class SmartArgsHandler:
    def __init__(self, function: Callable, need_to_handle_positional_args: bool = False):
        """Handles smart function arguments

        :param function: function that can contain smart arguments
        :param need_to_handle_positional_args: if False, then only kwargs-only parameters will be processed.
             All other parameters, including those that can be both positional and named,
             are considered positional here. This is consistent with the module inspect documentation.
        """
        self.__need_to_handle_positional_args = need_to_handle_positional_args

        full_arg_spec = inspect.getfullargspec(function)
        self.__positional_defaults = full_arg_spec.defaults or ()
        self.__positional_args = full_arg_spec.args
        self.__kwonly_defaults = full_arg_spec.kwonlydefaults or {}

        if not self.__need_to_handle_positional_args and any(
            isinstance(arg, Isolated) or isinstance(arg, Evaluated) for arg in self.__positional_defaults
        ):
            raise ValueError(
                "The default value of the positional parameter is a Smart argument, "
                "but the ability to handle them is disabled."
            )

        self.__number_of_positional_args_without_default = len(self.__positional_args) - len(self.__positional_defaults)

        self.__function = function
        update_wrapper(self, function)

    def __handle_kwonly_args(self, kwargs: Dict[str, Any]) -> None:
        """
        Changes the value of kwargs by changing the current arguments

        :param kwargs: dictionary containing current arguments
        """
        for key in self.__kwonly_defaults:
            if isinstance(self.__kwonly_defaults[key], SmartArgument):
                kwargs[key] = self.__kwonly_defaults[key].get_new_argument(kwargs[key] if key in kwargs else None)

    def __handle_positional_args(self, args_as_list: List, kwargs: Dict[str, Any]) -> None:
        """
        Changes the value of kwargs and args_as_list, changing the current arguments

        :param args_as_list: list containing current positional arguments
        :param kwargs: dictionary containing current keyword arguments
        """
        args_as_list_len = len(args_as_list)
        for index, value in enumerate(self.__positional_defaults):
            index_in_args = index + self.__number_of_positional_args_without_default
            if args_as_list_len > index_in_args:
                if isinstance(value, SmartArgument):
                    args_as_list[index_in_args] = value.get_new_argument(args_as_list[index_in_args])
            elif self.__positional_args[index_in_args] in kwargs:
                key = self.__positional_args[index_in_args]
                args_as_list += (
                    [value.get_new_argument(kwargs[key])] if isinstance(value, SmartArgument) else [kwargs[key]]
                )
                kwargs.pop(key)
            else:
                args_as_list += [value.get_new_argument(None)] if isinstance(value, SmartArgument) else [value]

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        args_as_list = list(args)

        self.__handle_kwonly_args(kwargs)

        if self.__need_to_handle_positional_args:
            self.__handle_positional_args(args_as_list, kwargs)
        return self.__function(*args_as_list, **kwargs)


def smart_args(function: Optional[Callable] = None, *, need_to_handle_positional_args: bool = False) -> Callable:
    """
    Decorator that supports smart argument handling

    :param function: function to handle smart arguments
    :param need_to_handle_positional_args: if False, then only kwargs-only parameters will be processed.
        All other parameters, including those that can be both positional and named,
        are considered positional here.
    """
    if function is None:
        return lambda func: SmartArgsHandler(func, need_to_handle_positional_args)

    return SmartArgsHandler(function, need_to_handle_positional_args)
