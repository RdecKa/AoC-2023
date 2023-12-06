import math
import re
from aoclib.puzzle import Puzzle

number_regex = re.compile(r"[0-9]+")


def parse_input1(lines):
    times = [int(x) for x in number_regex.findall(next(lines))]
    distances = [int(x) for x in number_regex.findall(next(lines))]
    return zip(times, distances)


def parse_input2(lines):
    time = int("".join(number_regex.findall(next(lines))))
    distance = int("".join(number_regex.findall(next(lines))))
    return (time, distance)


def count_winning_strategies(game):
    # Quadratic inequality
    (total_time, dist) = game
    d = total_time**2 - 4 * dist
    # Ensure distance > record (not just >=)
    lowest_solution = math.floor((total_time - math.sqrt(d)) / 2 + 1)
    highest_solution = math.ceil((total_time + math.sqrt(d)) / 2 - 1)
    return highest_solution - lowest_solution + 1


class Day6(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 4568778
        self.star2_solution = 28973936

    def star1(self):
        product = 1
        for game in parse_input1(self.filereader.lines()):
            product *= count_winning_strategies(game)
        return product

    def star2(self):
        return count_winning_strategies(parse_input2(self.filereader.lines()))
