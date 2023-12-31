import re
from aoclib.puzzle import Puzzle


line_regex = re.compile(r"Card [0-9 ]+: ([0-9 ]+) \| ([0-9 ]+)")
number_regex = re.compile(r"[0-9]+")


def count_common_numbers(line):
    match = line_regex.match(line)
    winning_numbers = set(number_regex.findall(match.group(1)))
    numbers_i_have = set(number_regex.findall(match.group(2)))
    return len(winning_numbers.intersection(numbers_i_have))


def get_card_points(line):
    common = count_common_numbers(line)
    return 0 if common == 0 else 2 ** (common - 1)


class Day4(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 17803
        self.star2_solution = 5554894

    def star1(self):
        return sum(self.filereader.lines(get_card_points))

    def star2(self):
        common_numbers_count = list(self.filereader.lines(count_common_numbers))
        card_count = [1 for _ in range(len(common_numbers_count))]
        for card_idx, common_count in enumerate(common_numbers_count):
            for received_card_idx in range(card_idx + 1, card_idx + common_count + 1):
                card_count[received_card_idx] += card_count[card_idx]
        return sum(card_count)
