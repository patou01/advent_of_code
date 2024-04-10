import math
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
    """
    Apparently, they will all cycle. So we should run each of them, whenever they land on a xxZ item, we save that one
    and check how many steps. Then it's a matter of least common multiple.
    Seems I was wrong with where I counted the step as well.
    Not a fun one.
    """
    current_keys = [key for key in data.steps if key.endswith("A")]
    current_points = [data.steps[key] for key in current_keys]
    step = 0
    seq_len = len(data.sequence)

    finished = False
    cycle_lengths = [[] for _ in current_keys]  # for cycle_lengths[0][1] is the 2nd cycle length for ghost 0
    cycle_ends = [[] for _ in current_keys]  # for cycle_ends[0][0] is the 2nd "end" for ghost 0, just to double check that they're all the same.

    while not finished:
        to_step = data.sequence[step % seq_len]
        update_points(to_step, current_points, current_keys, data)
        step += 1
        for n, key in enumerate(current_keys):
            if key.endswith("Z"):
                cycle_lengths[n].append(key)
                cycle_ends[n].append(step)
        keys_z = [key for key in current_keys if key.endswith("Z")]
        finished = len(current_keys) == len(keys_z)

        # assume that 100000 is enough runs to find a cycle length for all.
        if step > 100000:
            finished = True

    for j, cycle in enumerate(cycle_lengths):
        end_0 = cycle[0]
        print(f"Ghost {j} ends up on {end_0}. Went {len(cycle)} times!")
        for n, cyc in enumerate(cycle):
            if n > 0:
                if cyc != end_0:
                    print("different!")

    for j, cycle in enumerate(cycle_ends):
        len_0 = cycle[0]
        print(f"Ghost {j} takes {len_0}. Went {len(cycle)} times!")
        for n, cyc in enumerate(cycle):
            if n > 0:
                if cyc - (n+1)*len_0 != 0:
                    print("different lengths!")

    mult = math.lcm(*[item[0] for item in cycle_ends])

    print(mult)


entry = read_file(__file__, "input")
container = Data(entry)
part_2(container)
