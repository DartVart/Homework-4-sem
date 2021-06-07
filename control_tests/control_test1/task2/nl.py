from typing import Optional


def print_result(index: int, line: str):
    output_line = f"\t{index}\t{line}"
    print(output_line, end="" if line[-1] == "\n" else "\n")


def nl(file_path: Optional[str] = None) -> None:
    if file_path is None:
        line_counter = 0
        print("Enter lines (for exit enter 'exit'):")
        line = input()
        while line != "exit":
            line_counter += 1
            print_result(line_counter, line)
            line = input()
        else:
            return
    try:
        with open(file_path) as file:
            for index, line in enumerate(file):
                print_result(index + 1, line)
    except FileNotFoundError:
        print(f"File {file_path} not found.")


if __name__ == "__main__":
    nl("res/some_text.txt")
