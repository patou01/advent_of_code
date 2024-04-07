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


def update_points(to_step: str, current_points: List[Step], current_keys: List[str], data: Data):
    for n, point in enumerate(current_points):
        if to_step == "R":
            key = point.right
        elif to_step == "L":
            key = point.left
        else:
            raise ValueError("wtf")
        current_points[n] = data.steps[key]
        current_keys[n] = key


def part_2(data: Data):
    current_keys = [key for key in data.steps if key.endswith("A")]
    current_points = [data.steps[key] for key in current_keys]
    step = 0
    seq_len = len(data.sequence)

    finished = False
    while not finished:
        to_step = data.sequence[step % seq_len]
        update_points(to_step, current_points, current_keys, data)
        keys_z = [key for key in current_keys if key.endswith("Z")]
        finished = len(current_keys) == len(keys_z)
        step += 1

    print(step)


entry = read_file(__file__, "test_2")
container = Data(entry)
part_2(container)
