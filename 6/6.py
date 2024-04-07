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
        return f"duration: {self.duration}, record: {self.record}"

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
        self.desc = desc

        self.races_1 = self.parse_one()
        self.race_2 = self.parse_two()

    def parse_one(self):
        times_strings = self.desc[0].split(":")[-1].split(" ")
        distances_strings = self.desc[1].split(":")[-1].split(" ")

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
        return [Race(time, distance) for time, distance in zip(times, distances)]

    def parse_two(self):
        time = int(self.desc[0].split(":")[-1].replace(" ", ""))
        distance = int(self.desc[1].split(":")[-1].replace(" ", ""))

        return Race(time, distance)


def part_1(data: Data):
    total = 1
    for race in data.races_1:
        total *= race.optimize()

    print(f"Part 1: {total}")


def part_2(data: Data):
    print(data.race_2)
    print(data.race_2.optimize())


entry = read_file(__file__, "test")
container = Data(entry)
part_1(container)
part_2(container)
