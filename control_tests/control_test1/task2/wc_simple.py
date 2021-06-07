from typing import List, Optional, Tuple


def process_file(filepath: str) -> Tuple[int, int, int]:
    lines = 0
    words = 0
    number_of_bytes = 0
    with open(filepath) as file:
        for line in file:
            lines += 1
            words += len(line.split())
            number_of_bytes += len(line.encode("utf-8"))
    return lines, words, number_of_bytes


def print_result(stats, file_path):
    stats_as_string = "\t".join(map(lambda x: str(x), stats))
    print(f"{stats_as_string}\t{file_path}")


def wc_with_stdin():
    print("Enter lines (to display stats enter 'exit'):")
    line = input()
    lines = 0
    words = 0
    number_of_bytes = 0
    while line != "exit":
        lines += 1
        words += len(line.split())
        number_of_bytes += len(line.encode("utf-8"))
        line = input()
    else:
        print(f"{lines}\t{words}\t{number_of_bytes}")


def wc(file_paths: Optional[List[str]] = None) -> None:
    if file_paths is None:
        wc_with_stdin()
        return

    total_values = [0, 0, 0]

    need_total_values = len(file_paths) > 1

    for filepath in file_paths:
        try:
            result = process_file(filepath)
            if need_total_values:
                for index, value in enumerate(result):
                    total_values[index] += value
            print_result(result, filepath)
        except FileNotFoundError:
            print(f"File {filepath} not found.")

    if need_total_values:
        print_result(total_values, "total")


if __name__ == "__main__":
    wc(["res/some_text.txt", "res/some_text_2.txt"])
