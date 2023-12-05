import re
from aoclib.puzzle import Puzzle

seeds_regex = re.compile(r"seeds: (.*)")
rule_regex = re.compile(r"([0-9]+) ([0-9]+) ([0-9]+)")


class AlmanacMap:
    def __init__(self) -> None:
        self.rules: (int, int, int) = []

    def add_rule(self, rule: (int, int, int)):
        self.rules.append(rule)

    def map(self, source: int) -> int:
        for dest_start, source_start, range_len in self.rules:
            if source_start <= source < source_start + range_len:
                return dest_start + (source - source_start)
        return source


class Almanac:
    def __init__(self, seeds, maps) -> None:
        self.seeds = seeds
        self.maps = maps

    def map(self, source: int) -> int:
        dest = source
        for m in self.maps:
            dest = m.map(dest)
        return dest


def parse_input(lines):
    seeds = [int(s) for s in seeds_regex.match(next(lines)).group(1).split(" ")]
    maps = []
    next(lines)  # Empty line
    end_reached = False
    while not end_reached:
        next(lines)  # Map name
        almanac_map = AlmanacMap()
        rule = next(lines)
        while rule != "":
            parts = rule_regex.match(rule)
            almanac_map.add_rule(
                (int(parts.group(1)), int(parts.group(2)), int(parts.group(3)))
            )
            try:
                rule = next(lines)
            except StopIteration:
                end_reached = True
                break
        maps.append(almanac_map)
    return Almanac(seeds, maps)


class Day5(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.almanac = parse_input(self.filereader.lines())

        self.star1_solution = 111627841
        self.star2_solution = None

    def star1(self):
        return min(self.almanac.map(seed) for seed in self.almanac.seeds)

    def star2(self):
        return 0
