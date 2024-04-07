import re
from dataclasses import dataclass
from typing import List

from utils import read_file


@dataclass
class Race:
    duration: int
    record: int
    speed_per_charge: int = 1  # maybe part 2 won't have 1

    def __str__(self):
        return f"duration: {self.duration}, record: {self.record}, beaten {self.optimize()} times"

    def optimize(self) -> int:
        i = 0
        for charge_time in range(self.duration):
            speed = charge_time * self.speed_per_charge
            distance = (self.duration - charge_time) * speed
            if distance > self.record:
                i += 1

        return i


class Data:
    """
    Parse the input. Basically we get 2 strings and just need to make pairs
    """
    def __init__(self, desc: List[str]):
        times_strings = desc[0].split(":")[-1].split(" ")
        distances_strings = desc[1].split(":")[-1].split(" ")

        reg_int = re.compile(r'^([\s\d]+)$')

        times = []
        distances = []
        for time in times_strings:
            reg = reg_int.match(time)
            if reg:
                times.append(int(reg.groups()[0]))

        for distance in distances_strings:
            reg = reg_int.match(distance)
            if reg:
                distances.append(int(reg.groups()[0]))

        assert len(times) == len(distances)
        self.races = [Race(time, distance) for time, distance in zip(times, distances)]


def part_1(data: Data):
    total = 1
    for race in data.races:
        total *= race.optimize()

    print(f"Part 1: {total}")


def part_2(data: Data):
    pass


entry = read_file(__file__, "input")
container = Data(entry)
part_1(container)
part_2(container)
