import os


def read_file(where_from: str, file: str):
    with open(os.path.join(os.path.dirname(where_from), file), "r") as f:
        return f.readlines()
