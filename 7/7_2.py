"""
Copied from part 1, but there's quite some change to apply in calculations,
and I don't want to override lt in a weird way that would be dependent on some
global variable.
"""
from dataclasses import dataclass
from typing import List

from utils import read_file


HAND_VALUES = {
    "FIVE_OF_A_KIND": 7,
    "FOUR_OF_A_KIND": 6,
    "FULL_HOUSE": 5,
    "THREE_OF_A_KIND": 4,
    "TWO_PAIR": 3,
    "ONE_PAIR": 2,
    "HIGH_CARD": 1
}

CARD_VALUES = {"J": 1,
               "2": 2,
               "3": 3,
               "4": 4,
               "5": 5,
               "6": 6,
               "7": 7,
               "8": 8,
               "9": 9,
               "T": 10,
               "Q": 11,
               "K": 12,
               "A": 13}

@dataclass
class Hand:
    cards: str
    bid: int

    def __post_init__(self):
        self.hand_dict = {}
        for card in self.cards:
            if card not in self.hand_dict:
                self.hand_dict[card] = 1
            else:
                self.hand_dict[card] += 1

        self.hand_type = self.parse_type()

    def parse_type(self) -> str:
        keys = list(self.hand_dict.keys())

        # if J is found in the keys, we allocate its amount to the type of card we had the most of
        if "J" in keys:
            to_add = self.hand_dict["J"]
            keys.remove("J")
            del self.hand_dict["J"]
            max_val = 0
            max_key = ""
            for key, value in self.hand_dict.items():
                if value > max_val:
                    max_val = value
                    max_key = key

            if len(keys) == 0:
                # edge case with only J...
                self.hand_dict["2"] = to_add
            else:
                self.hand_dict[max_key] += to_add
            keys = list(self.hand_dict.keys())  # refresh the keys
        match len(keys):
            case 1:
                return "FIVE_OF_A_KIND"
            case 2:
                if self.hand_dict[keys[0]] in [1, 4]:
                    return "FOUR_OF_A_KIND"
                else:
                    return "FULL_HOUSE"
            case 3:
                if self.hand_dict[keys[0]] == 3 or self.hand_dict[keys[1]] == 3 or self.hand_dict[keys[2]] == 3:
                    return "THREE_OF_A_KIND"
                else:
                    return "TWO_PAIR"
            case 4:
                return "ONE_PAIR"
            case 5:
                return "HIGH_CARD"

    def __str__(self):
        return f"{self.cards} {self.bid}"

    def __lt__(self, other):
        return self.compare(other) < 0

    def __ge__(self, other):
        return self.compare(other) > 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def compare(self, other):
        delta = HAND_VALUES[self.hand_type] - HAND_VALUES[other.hand_type]
        if delta != 0:
            return delta
        for n, _ in enumerate(self.cards):
            delta = CARD_VALUES[self.cards[n]] - CARD_VALUES[other.cards[n]]
            if delta != 0:
                return delta

class Data:
    """
    Parse the input.
    """
    def __init__(self, desc: List[str]):
        self.hands = []
        for line in desc:
            split = line.split(" ")
            self.hands.append(Hand(split[0], int(split[1])))

        for hand in self.hands:
            print(hand)


def part_1(data: Data):
    total = 0
    hands = sorted(data.hands)
    print("sorting")
    for n, hand in enumerate(hands):
        print(f"{hand}, rank {n+1}")
        total += (n+1)*hand.bid

    print(f"Part 1: {total}")


entry = read_file(__file__, "input")
container = Data(entry)
part_1(container)

