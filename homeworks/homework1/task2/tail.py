from argparse import ArgumentParser
from collections import deque
from typing import List


def get_tail_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "-n", "--lines", default=10, type=int, help="[NUM] output the last NUM lines, instead of the last 10"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", default=False, help="never output headers giving file names"
    )
    parser.add_argument("file_paths", type=str, nargs="+", help="files for processing. There must be at least one file")
    return parser


def tail(file_paths: List[str], quiet: bool = False, lines: int = 10) -> None:
    need_to_show_headers = not quiet and len(file_paths) > 1
    for filepath in file_paths:
        try:
            with open(filepath) as file:
                if need_to_show_headers:
                    print(f"==> {filepath} <==")
                for line in deque(file, maxlen=lines):
                    print(line if line[-1] == "\n" else f"{line}\n", end="")
        except FileNotFoundError:
            print(f"File {filepath} not found.")


if __name__ == "__main__":
    args = vars(get_tail_parser().parse_args())
    tail(**args)
