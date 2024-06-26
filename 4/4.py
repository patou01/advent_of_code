from dataclasses import dataclass
from typing import List, Tuple

from utils import read_file


class Card:
    def __init__(self, descriptor: str):
        id_game = descriptor.split(":")
        self.id = int(id_game[0].split(" ")[-1])
        numbers = id_game[1].split("|")
        win = self.clear_numbers(numbers[0]).split(" ")
        ours = self.clear_numbers(numbers[1]).split(" ")
        self.winning_numbers = [int(number) for number in win]
        self.our_numbers = [int(number) for number in ours]

    def clear_numbers(self, numbers: str) -> str:
        return numbers.lstrip(" ").rstrip(" ").replace("  ", " ")

    def get_points(self) -> Tuple[int, int]:
        good_numbers = []  # maybe useful for part 2
        points = 0
        for number in self.our_numbers:
            if number in self.winning_numbers:
                if len(good_numbers) < 1:
                    points += 1
                else:
                    points *= 2
                good_numbers.append(number)

        return points, len(good_numbers)


def part_1(data: List[Card]):
    total = 0
    for card in data:
        total += card.get_points()[0]

    print(f"Part 1: {total}")


def part_2(data: List[Card]):
    """
    naive brute force, takes like 2 minutes to run, amazing skills.
    Could just do the maths and then it's probably about a second.
    :param data:
    :return:
    """
    new_cards = data.copy()
    for n, card in enumerate(new_cards):
        to_create = card.get_points()[1]  # number of cards to create after this one
        for j in range(to_create):
            new_cards.append(data[card.id+j])

    print(f"Part 2: {len(new_cards)}")


entry = read_file(__file__, "input")
cards = [Card(line) for line in entry]
part_1(cards)
part_2(cards)
