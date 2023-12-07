from functools import cmp_to_key
from aoclib.puzzle import Puzzle
from enum import IntEnum
from collections import defaultdict

no_joker = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
with_joker = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


class HandType(IntEnum):
    FIVE_KIND = 7
    FOUR_KIND = 6
    FULL_HOUSE = 5
    THREE_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class Hand:
    def __init__(self, hand_str: str, bid: int, play_with_joker: bool) -> None:
        self.hand_str = hand_str
        self.bid = bid
        self.type = self.get_hand_type(hand_str, play_with_joker)

    def __repr__(self):
        return f"({self.type.name}, {self.hand_str})"

    def get_hand_type(self, hand_str, play_with_joker):
        d = defaultdict(int)
        for char in hand_str:
            d[char] += 1
        num_unique_cards = len(d.items())
        highest_frequency = max(d.values())

        if play_with_joker:
            # Add all jokers to the card with the highest frequency
            joker_count = d["J"]
            if joker_count == 5:
                num_unique_cards = 1
                highest_frequency = 5
            elif joker_count > 0:
                num_unique_cards -= 1
                # Special case: joker is the most frequent card and all other
                # cards are less frequent
                highest_frequency = (
                    max(freq for (card, freq) in d.items() if card != "J") + joker_count
                )

        match num_unique_cards:
            case 1:
                return HandType.FIVE_KIND
            case 2:
                match highest_frequency:
                    case 4:
                        return HandType.FOUR_KIND
                    case 3:
                        return HandType.FULL_HOUSE
            case 3:
                match highest_frequency:
                    case 3:
                        return HandType.THREE_KIND
                    case 2:
                        return HandType.TWO_PAIR
            case 4:
                return HandType.ONE_PAIR
            case 5:
                return HandType.HIGH_CARD

        raise AssertionError


def parse_line(line, play_with_joker):
    hand, bid = line.split(" ")
    return Hand(hand, int(bid), play_with_joker)


def compare_hands_generator(card_order):
    def compare_hands(h1: Hand, h2: Hand):
        """
        Returns negative value if h1 is weaker than h2, and positive value if
        h1 is stronger than h2
        """
        if h1.type != h2.type:
            return h1.type - h2.type
        for c1, c2 in zip(h1.hand_str, h2.hand_str):
            if c1 != c2:
                return card_order.index(c2) - card_order.index(c1)
        raise AssertionError  # Hands are equal

    return compare_hands


def calculate_score(hands: list[Hand], card_order):
    sorted_hands = sorted(hands, key=cmp_to_key(compare_hands_generator(card_order)))
    result = 0
    for i, hand in enumerate(sorted_hands):
        result += (i + 1) * hand.bid
    return result


class Day7(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 247815719
        self.star2_solution = 248747492

    def star1(self):
        hands = list(self.filereader.lines(lambda x: parse_line(x, False)))
        return calculate_score(hands, no_joker)

    def star2(self):
        hands = list(self.filereader.lines(lambda x: parse_line(x, True)))
        return calculate_score(hands, with_joker)
