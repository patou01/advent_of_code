from dataclasses import dataclass
from typing import List

from utils import read_file
from string import punctuation

symbols = list(punctuation)
symbols.remove(".")


def is_integer(char: str):
    try:
        int(char)
        return True
    except:
        return False


@dataclass
class Point:
    item: str
    x: int
    y: int

    def __str__(self):
        return f"{self.item} at x: {self.x}, y: {self.y}"


@dataclass
class Number:
    x: int
    y: int
    chars: str

    def __str__(self):
        return f"{self.chars} at x: {self.x}, y: {self.y}"

    @property
    def integer(self):
        return int(self.chars)

    @property
    def length(self):
        return len(self.chars)

    def is_in_contact(self, x, y):
        """
        Returns whether this number touches the cell at x,y.
        :param x:
        :param y:
        :return:
        """
        if not (self.y - 1 <= y <= self.y + 1):
            return False

        if not (self.x - 1 <= x <= self.x + self.length):
            return False
        return True

class Map:
    def __init__(self, data: List[str]):
        for line in data:
            print(line)
        self.data = data
        self.numbers = []
        self.find_numbers()
        self.symbols = self.find_symbols()

    def find_numbers(self):
        for y, line in enumerate(self.data):
            for x, char in enumerate(line):
                if is_integer(char) and self.integer_is_not_found(x, y):
                    i = 0
                    while x+i < len(line) and is_integer(line[x+i]):
                        i += 1
                    self.numbers.append(Number(x, y, line[x:x+i]))

    def find_symbols(self) -> List[Point]:
        ret = []
        for y, line in enumerate(self.data):
            for x, char in enumerate(line):
                if char in symbols:
                    ret.append(Point(char, x, y))
        return ret

    def integer_is_not_found(self, x, y):
        for number in self.numbers:
            if number.y == y:
                if number.x < x <= number.x + len(number.chars):
                    return False
        return True


def part_1(schema: Map):
    relevant_numbers = []
    for symbol in schema.symbols:
        for number in schema.numbers:
            if number.is_in_contact(symbol.x, symbol.y):
                relevant_numbers.append(number)

    summed = 0
    for number in relevant_numbers:
        print(number)
        summed += number.integer
    print(f"Part 1: {summed}")


def part_2(schema: Map):
    ratio = 0
    for symbol in schema.symbols:
        if symbol.item == "*":  # gears
            in_contact_with: List[Number] = []
            for number in schema.numbers:
                if number.is_in_contact(symbol.x, symbol.y):
                    in_contact_with.append(number)

            if len(in_contact_with) == 2:
                ratio += in_contact_with[0].integer * in_contact_with[1].integer
    print(f"Part 2 {ratio}")


entry = read_file(__file__, "input")
schematic = Map(entry)
part_1(schematic)
part_2(schematic)
