from argparse import ArgumentParser
from typing import Dict, List, Callable, Set, TypeVar

K = TypeVar("K")
V = TypeVar("V")


def print_result(dictionary: Dict[K, V], key_order: List[K], ending: str) -> None:
    print("\t".join([str(dictionary[k]) for k in key_order if k in dictionary] + [ending]))


def get_wc_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("-l", "--lines", action="store_true", default=False, help="print the newline counts")
    parser.add_argument("-w", "--words", action="store_true", default=False, help="print the word counts")
    parser.add_argument("-m", "--chars", action="store_true", default=False, help="print the character counts")
    parser.add_argument("-c", "--bytes", action="store_true", default=False, help="print the byte counts")
    parser.add_argument(
        "-L", "--max-line-length", action="store_true", default=False, help="print the maximum line width"
    )
    parser.add_argument("file_paths", type=str, nargs="+", help="files for processing. There must be at least one file")
    return parser


def process_file(
    filepath: str, handlers: Dict[str, Callable[[int, str], int]], required_options: Set[str]
) -> Dict[str, int]:
    """
    :param filepath: The path to the file
    :param handlers: A dictionary in which each option (key) has its own function
        that processes the string by changing some integer value.
    :param required_options: Options that will be involved in processing.
    :return: A dictionary in which each option has an integer calculated by the corresponding function.
    """
    results = {option: 0 for option in required_options}
    with open(filepath) as file:
        for line in file:
            for option in handlers:
                if option in required_options:
                    results[option] = handlers[option](results[option], line)
    return results


def wc(file_paths: List[str], options: Set[str]) -> None:
    """
    :param file_paths: Filepath list
    :param options: A set that will contain options,
        referred to as the long parameter names of the "wc" bash-command:
        "lines", "words", "chars", "bytes", "max_line_length".
    """

    if not options:
        options = {"lines", "words", "chars"}

    total_values = {}

    need_total_values = len(file_paths) > 1
    if need_total_values:
        total_values = {option: 0 for option in options}

    handlers = {
        "lines": lambda x, _: x + 1,
        "words": lambda x, cur_line: x + len(cur_line.split()),
        "chars": lambda x, cur_line: x + len(cur_line),
        "bytes": lambda x, cur_line: x + len(cur_line.encode("utf-8")),
        "max_line_length": lambda x, cur_line: max(x, len(cur_line.rstrip())),
    }
    output_order = ["lines", "words", "chars", "bytes", "max_line_length"]

    for filepath in file_paths:
        cur_values = {}
        try:
            cur_values = process_file(filepath, handlers, options)
            print_result(cur_values, output_order, filepath)
        except FileNotFoundError:
            print(f"File {filepath} not found.")

        if need_total_values:
            total_values = {
                option: total_values[option] + cur_values[option]
                if option != "max_line_length"
                else max(total_values[option], cur_values[option])
                for option in total_values
            }

    if need_total_values:
        print_result(total_values, output_order, "total")


if __name__ == "__main__":
    args = vars(get_wc_parser().parse_args())
    wc(args["file_paths"], {param for param in args if isinstance(args[param], bool) and args[param]})
