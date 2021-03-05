from argparse import ArgumentParser
from typing import List


def get_head_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "-n", "--lines", default=10, type=int, help="[NUM] print the first NUM lines instead of the first 10"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", default=False, help="never print headers giving file names"
    )
    parser.add_argument("file_paths", type=str, nargs="+", help="files for processing. There must be at least one file")
    return parser


def head(file_paths: List[str], quiet: bool = False, lines: int = 10) -> None:
    need_to_show_headers = not quiet and len(file_paths) > 1
    for filepath in file_paths:
        try:
            with open(filepath) as file:
                if need_to_show_headers:
                    print(f"==> {filepath} <==")
                for index, line in enumerate(file, start=1):
                    if index > lines:
                        break
                    print(line if line[-1] == "\n" else f"{line}\n", end="")
        except FileNotFoundError:
            print(f"File {filepath} not found.")


if __name__ == "__main__":
    args = vars(get_head_parser().parse_args())
    head(**args)
