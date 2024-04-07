from dataclasses import dataclass
from typing import List, Tuple

from utils import read_file


class ShortMap:
    def __init__(self, descriptor: str):
        split = [int(number) for number in descriptor.split(" ")]
        self.destination = split[0]
        self.source = split[1]
        self.length = split[2]

    def can_map(self, thing: int):
        return self.source <= thing < self.source + self.length

    def map(self, thing: int) -> int:
        if self.can_map(thing):
            return self.destination + (thing - self.source)

    def revert_map(self, thing: int) -> int:
        if self.can_revert_map(thing):
            return self.source + (thing - self.destination)

    def can_revert_map(self, thing: int) -> bool:
        return self.destination <= thing < self.destination + self.length


class Map:
    def __init__(self, descriptor: List[str]):
        self.sub_maps = [ShortMap(desc) for desc in descriptor]

    def map(self, value: int):
        for sub_map in self.sub_maps:
            if sub_map.can_map(value):
                return sub_map.map(value)
        return value

    def revert_map(self, value: int):
        for sub_map in self.sub_maps:
            if sub_map.can_revert_map(value):
                return sub_map.revert_map(value)
        return value


class DataContainer:
    seeds: List[int]
    seed_to_soil: Map
    soil_to_fertilizer: Map
    fertilizer_to_water: Map
    water_to_light: Map
    light_to_temp: Map
    temp_to_hum: Map
    hum_to_loc: Map

    def __init__(self, descriptor: List[str]):
        self.descriptor = descriptor
        split_seeds = descriptor[0].split(":")[1].lstrip(" ").split(" ")
        self.seeds = [int(seed) for seed in split_seeds]
        mappings = self.get_mapping_locations()
        self.seed_to_soil = self._parse_map(mappings[0])
        self.soil_to_fertilizer = self._parse_map(mappings[1])
        self.fertilizer_to_water = self._parse_map(mappings[2])
        self.water_to_light = self._parse_map(mappings[3])
        self.light_to_temp = self._parse_map(mappings[4])
        self.temp_to_hum = self._parse_map(mappings[5])
        self.hum_to_loc = self._parse_map(mappings[6])

    def get_mapping_locations(self):
        maps = []
        start = 0
        end = 0
        for n, line in enumerate(self.descriptor):
            if line.endswith("map:"):
                start = n
                end = 0
            if line == "" or n == len(self.descriptor)-1:
                end = n

            if end > 1:
                maps.append((start, end))

        return maps

    def _parse_map(self, tup: Tuple[int, int]):
        return Map(self.descriptor[tup[0]+1:tup[1]])

    def map_to_location(self, seed: int):
        """
        kinda yikes
        """
        return self.hum_to_loc.map(
                    self.temp_to_hum.map(
                        self.light_to_temp.map(
                            self.water_to_light.map(
                                self.fertilizer_to_water.map(
                                    self.soil_to_fertilizer.map(
                                        self.seed_to_soil.map(seed)
                                    )
                                )
                            )
                        )
                    )
                )

    def map_to_seed(self, location: int):
        return self.seed_to_soil.revert_map(
                    self.soil_to_fertilizer.revert_map(
                        self.fertilizer_to_water.revert_map(
                            self.water_to_light.revert_map(
                                self.light_to_temp.revert_map(
                                    self.temp_to_hum.revert_map(
                                        self.hum_to_loc.revert_map(location)
                                    )
                                )
                            )
                        )
                    )
                )


def part_1(data: DataContainer):
    locations = [data.map_to_location(seed) for seed in data.seeds]
    print(f"Part 1: {min(locations)}")


def part_2(data: DataContainer):
    """
    For part 2, we reverse the mapping. Start searching from location 0 to see if has a seed in our ranges.
    Then we increment. As soon as we've found one, we have the lowest location possible for one of our seeds.
    """
    i = 0
    ranges = []
    for n, seed in enumerate(data.seeds):
        if n % 2 == 0:
            ranges.append(range(seed, seed + data.seeds[n+1]))
    found = False
    while not found:
        seed = data.map_to_seed(i)
        i += 1
        for item in ranges:
            if not found:
                if seed in item:
                    found = True
                    break

    print(f"part 2: {i-1}")


entry = read_file(__file__, "input")
container = DataContainer(entry)
part_1(container)
part_2(container)
