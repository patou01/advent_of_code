import copy
from typing import List

from utils import read_file


class Series:
    def __init__(self, desc: str):
        self.desc = desc
        self.data = [int(thing) for thing in self.desc.split(" ")]
        self.diffs = []

    def find_next(self):
        """
        First do all the diffs, then walk it back up.
        """
        self.diffs = [self.diff(self.data)]
        # sneaky that they added negatives...
        while not ((self.diffs[-1][0] == 0) and self.diffs.count(self.diffs[-1]) == len(self.diffs[-1])):
            self.diffs.append(self.diff(self.diffs[-1]))

        self.diffs[-1].append(0)
        length = len(self.diffs)
        rev = list(reversed(self.diffs))

        for n, diff in enumerate(rev):
            if n < length - 1:
                last_value = rev[n+1][-1] + rev[n][-1]
                rev[n+1].append(last_value)

        new = copy.deepcopy(self.data)
        new.append(self.data[-1] + self.diffs[0][-1])
        return new

    def diff(self, int_list) -> List[int]:
        diff = []
        for n, item in enumerate(int_list):
            if n < len(int_list) - 1:
                diff.append(int_list[n+1]-int_list[n])

        return diff

    def find_previous(self) -> List[int]:
        """
            First do all the diffs, then walk it back up.
        """
        self.diffs = [self.backwards_diff(self.data)]
        # sneaky that they added negatives...
        while not ((self.diffs[-1][0] == 0) and self.diffs.count(self.diffs[-1]) == len(self.diffs[-1])):
            self.diffs.append(self.backwards_diff(self.diffs[-1]))

        self.diffs[-1].append(0)
        length = len(self.diffs)
        rev = list(reversed(self.diffs))

        for n, diff in enumerate(rev):
            if n < length - 1:
                first_value = rev[n + 1][0] - rev[n][0]
                rev[n + 1].insert(0, first_value)

        new = copy.deepcopy(self.data)
        new.insert(0, self.data[0] - self.diffs[0][0])
        return new

    def backwards_diff(self, int_list) -> List[int]:
        diff = []
        for n, item in enumerate(int_list):
            if n > 0:
                diff.append(int_list[n] - int_list[n-1])
        return diff


class Data:
    def __init__(self, desc: List[str]):
        self.desc = desc
        self.series = [Series(line) for line in self.desc]


def part_1(data: Data):
    result = 0
    for n, series in enumerate(data.series):
        new = series.find_next()
        result += new[-1]

    print(f"Part 1: {result}")


def part_2(data: Data):
    result = 0
    for n, series in enumerate(data.series):
        new = series.find_previous()
        result += new[0]

        if n == 2:
            print(new)
            for diff in series.diffs:
                print(diff)

    print(f"Part 2: {result}")


entry = read_file(__file__, "input")
container = Data(entry)
part_1(container)
part_2(container)
