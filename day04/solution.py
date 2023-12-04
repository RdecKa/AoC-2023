import re
from aoclib.puzzle import Puzzle


line_regex = re.compile(r"Card [0-9 ]+: ([0-9 ]+) \| ([0-9 ]+)")
number_regex = re.compile(r"[0-9]+")


def get_card_points(line):
    match = line_regex.match(line)
    winning_numbers = set(number_regex.findall(match.group(1)))
    numbers_i_have = set(number_regex.findall(match.group(2)))
    common = winning_numbers.intersection(numbers_i_have)
    if len(common) == 0:
        return 0
    return 2 ** (len(common) - 1)


class Day4(Puzzle):
    def star1(self):
        return sum(self.filereader.lines(get_card_points))

    def star2(self):
        return 0
