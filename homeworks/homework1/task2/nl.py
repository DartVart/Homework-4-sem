from argparse import ArgumentParser
from typing import List


def get_nl_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("-i", "--line-increment", default=1, type=int, help="[NUM] line number increment at each line")
    parser.add_argument(
        "-s", "--number-separator", default="\t", type=str, help="[STRING] add STRING after (possible) line number"
    )
    parser.add_argument("file_paths", type=str, nargs="+", help="files for processing. There must be at least one file")
    return parser


def nl(file_paths: List[str], number_separator: str = "\t", line_increment: int = 1) -> None:
    line_counter = 0
    for filepath in file_paths:
        try:
            with open(filepath) as file:
                for line in file:
                    if line.strip():
                        line_counter += line_increment
                        line = f"\t{line_counter}{number_separator}{line}"
                    print(line if line[-1] == "\n" else f"{line}\n", end="")
        except FileNotFoundError:
            print(f"File {filepath} not found.")


if __name__ == "__main__":
    args = vars(get_nl_parser().parse_args())
    nl(**args)
