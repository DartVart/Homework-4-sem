from collections import deque
from typing import List, Optional


def print_line(line: str):
    print(line, end="" if line[-1] == "\n" else "\n")


def tail(file_paths: Optional[List[str]] = None) -> None:
    if file_paths is None:
        print("Enter lines (to display last lines enter 'exit'):")
        line = input()
        lines_deque = deque(maxlen=10)
        while line != "exit":
            lines_deque.append(line)
            line = input()
        else:
            for line in lines_deque:
                print_line(line)
            return

    for file_path in file_paths:
        need_to_show_headers = len(file_paths) > 1
        try:
            with open(file_path) as file:
                if need_to_show_headers:
                    print(f"==> {file_path} <==")
                for line in deque(file, maxlen=10):
                    print_line(line)
        except FileNotFoundError:
            print(f"File {file_path} not found.")


if __name__ == "__main__":
    tail(["res/some_text.txt", "res/some_text_2.txt"])
