import sys


def print_error(message: str, source: str, lineno: int):
    print(message)
    lines = source.split("\n")
    print(">", lines[lineno-1])
    # print("  ", " " * index, "^", sep="")
    sys.exit(1)