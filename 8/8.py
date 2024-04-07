from typing import List

from utils import read_file


class Step:
    def __init__(self, desc: str):
        self.desc = desc
        left_right = desc.replace("(", "").replace(")", "").replace(",", "").split(" ")
        self.left = left_right[0]
        self.right = left_right[1]

    def __str__(self):
        return f" ({self.left}, {self.right})"


class Data:
    def __init__(self, desc: List[str]):
        self.desc = desc
        self.sequence = desc[0]
        self.steps = {}
        for n, line in enumerate(self.desc):
            if line and n > 1:
                split = line.split(" = ")
                self.steps[split[0]] = Step(split[1])


def part_1(data: Data):
    for key, val in data.steps.items():
        print(f"{key}: {val}")

    key = "AAA"
    step = 0
    seq_len = len(data.sequence)
    while key != "ZZZ":
        to_step = data.sequence[step % seq_len]
        current = data.steps[key]
        if to_step == "R":
            key = current.right
        else:
            key = current.left

        step += 1

    print(step)

def part_2(data: Data):
    pass


entry = read_file(__file__, "input")
container = Data(entry)
part_1(container)
part_2(container)
