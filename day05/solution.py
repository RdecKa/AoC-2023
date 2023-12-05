from operator import itemgetter
import re
from aoclib.puzzle import Puzzle

seeds_regex = re.compile(r"seeds: (.*)")
rule_regex = re.compile(r"([0-9]+) ([0-9]+) ([0-9]+)")


class AlmanacMap:
    def __init__(self) -> None:
        self.rules: (int, int, int) = []  # (dest_start, source_start, range_len)

    def add_rule(self, rule: (int, int, int)):
        self.rules.append(rule)

    def initialise(self):
        # Sort by source_start
        self.rules = sorted(self.rules, key=itemgetter(1))

        # Add missing identity rules (x => x)
        next_to_map = 0
        new_maps = []
        for _, source_start, range_len in self.rules:
            if source_start > next_to_map:
                new_maps.append((next_to_map, next_to_map, source_start - next_to_map))
            next_to_map = source_start + range_len

        # The last identity map is not included (because we don't know the length)
        self.rules = sorted(self.rules + new_maps, key=itemgetter(1))

    def map(self, source: int) -> int:
        for dest_start, source_start, range_len in self.rules:
            if source_start <= source < source_start + range_len:
                return dest_start + (source - source_start)
        return source

    def map_range(self, input_range):
        (range_start, remaining_len) = input_range
        mapped_ranges = []
        for dest_start, source_start, range_len in self.rules:
            if remaining_len == 0:
                break
            if source_start <= range_start < source_start + range_len:
                mapped_range_len = min(
                    range_len - (range_start - source_start), remaining_len
                )
                mapped_ranges.append(
                    (dest_start + (range_start - source_start), mapped_range_len)
                )
                remaining_len -= mapped_range_len
                range_start += mapped_range_len
        if remaining_len > 0:
            # This is identity mapping after the last rule
            mapped_ranges.append(
                ((range_start + remaining_len - remaining_len), remaining_len)
            )
        return mapped_ranges


class Almanac:
    def __init__(self, seeds, maps) -> None:
        self.seeds = seeds
        self.maps = maps

    def map(self, source: int) -> int:
        dest = source
        for m in self.maps:
            dest = m.map(dest)
        return dest

    def map_ranges(self):
        dest_ranges = self.get_seed_ranges()
        for m in self.maps:
            new_ranges = []
            for r in dest_ranges:
                new_ranges += m.map_range(r)
            dest_ranges = new_ranges
        return dest_ranges

    def get_seed_ranges(self):
        ranges = []
        for i in range(0, len(self.seeds), 2):
            ranges.append((self.seeds[i], self.seeds[i + 1]))
        return ranges


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
        almanac_map.initialise()
        maps.append(almanac_map)
    return Almanac(seeds, maps)


class Day5(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.almanac = parse_input(self.filereader.lines())

        self.star1_solution = 111627841
        self.star2_solution = 69323688

    def star1(self):
        return min(self.almanac.map(seed) for seed in self.almanac.seeds)

    def star2(self):
        lowest_range = min(self.almanac.map_ranges(), key=itemgetter(0))
        return lowest_range[0]
