from typing import List

from utils import read_file


class Throw:
    def __init__(self, description: str):
        cubes = description.split(",")
        self.blue = 0
        self.red = 0
        self.green = 0
        for cube in cubes:
            number_color = cube.replace("\n", "").split(" ")
            setattr(self, number_color[-1], int(number_color[1]))

    def is_possible(self, r: int, g: int, b: int):
        return self.red <= r and self.green <= g and self.blue <= b

    def __str__(self):
        return f"{self.red} red, {self.blue} blue, {self.green} green"


class Game:
    def __init__(self, description: str):
        """
        Description of a game is of shape
        "Game N: X cube, Y cube; Z cube, W cube"

        :param description:
        """
        self.description = description.replace("\n", "")
        id_game = description.split(":")
        self.id = int(id_game[0].split(" ")[-1])
        self.throws = [Throw(desc) for desc in id_game[1].split(";")]

    def is_possible(self, r: int, g: int, b: int):
        for throw in self.throws:
            if not throw.is_possible(r, g, b):
                return False
        return True

    def get_power(self):
        r = 0
        g = 0
        b = 0
        for throw in self.throws:
            r = max(r, throw.red)
            g = max(g, throw.green)
            b = max(b, throw.blue)

        return r*g*b


data = read_file(__file__, "input_1")
games: List[Game] = [Game(line) for line in data]

value = 0
for game in games:
    args = {"r": 12, "g": 13, "b": 14}
    possible = game.is_possible(**args)
    if possible:
        value += game.id

print(f"Part 1: {value}")

print(f"Part 2: {sum(game.get_power() for game in games)}")

