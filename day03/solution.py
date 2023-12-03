from collections import defaultdict
import sys
from aoclib.grid import BoolGrid, Grid, IntGrid
from aoclib.puzzle import Puzzle


def is_symbol(char):
    return char != "." and not char.isdigit()


class Schematic:
    def __init__(self, scheme) -> None:
        self.scheme = scheme

    def size(self) -> int:
        # The scheme is a square
        if len(self.scheme) != len(self.scheme[0]):
            raise AssertionError
        return len(self.scheme)

    def get_adjacency_mask(self, grid, predicate, val_func) -> Grid:
        mask = Grid(self.size(), self.size(), False)
        for rowi in range(self.size()):
            for coli in range(self.size()):
                if predicate(grid[rowi][coli]):
                    mask.set_adjacent_9_fields(rowi, coli, val_func(rowi, coli))
        return mask

    def sum_adjacent_numbers(self) -> int:
        adjacency_mask = self.get_adjacency_mask(
            self.scheme, is_symbol, lambda r, c: True
        )
        total = 0
        for rowi in range(self.size()):
            total += self.sum_adjacent_numbers_in_row(rowi, adjacency_mask)
        return total

    def sum_adjacent_numbers_in_row(self, rowi, adjacency_mask) -> int:
        total = 0
        number_str = ""
        is_adjacent = False
        for coli in range(self.size()):
            char = self.scheme[rowi][coli]
            if char.isdigit():
                number_str += char
                if adjacency_mask[rowi][coli]:
                    is_adjacent = True
            else:
                if number_str != "" and is_adjacent:
                    total += int(number_str)
                number_str = ""
                is_adjacent = False
        # Check last number (if the last symbol in the row was a digit)
        if number_str != "" and is_adjacent:
            total += int(number_str)
        return total

    def get_number_adjacency_mask(self) -> IntGrid:
        """For each cell in the grid, how many numbers are adjacent?"""
        mask = IntGrid(self.size(), self.size(), 0)
        increment_func = lambda x: x + 1
        for rowi in range(self.size()):
            number_started = False
            for coli in range(self.size()):
                if self.scheme[rowi][coli].isdigit():
                    # Modify cells in the right column
                    for drow in range(-1, 2):
                        mask.modify(rowi + drow, coli + 1, increment_func)
                    if not number_started:
                        # Modify cells in the left and current column
                        for drow in range(-1, 2):
                            mask.modify(rowi + drow, coli - 1, increment_func)
                            mask.modify(rowi + drow, coli, increment_func)
                    number_started = True
                else:
                    number_started = False
        return mask

    def find_gears(self) -> BoolGrid:
        number_adjacency_mask = self.get_number_adjacency_mask()
        mask = BoolGrid(self.size(), self.size(), False)
        for row in range(self.size()):
            for col in range(self.size()):
                if (
                    self.scheme[row][col] == "*"
                    and number_adjacency_mask[row][col] == 2
                ):
                    mask[row][col] = True
        return mask

    def get_gear_parts(self):
        gears = self.find_gears()
        gear_adjacency_mask = self.get_adjacency_mask(
            gears, lambda x: x, lambda r, c: (r, c)
        )
        parts = defaultdict(list)
        for rowi in range(self.size()):
            number_str = ""
            adjacent_to = None
            for coli in range(self.size()):
                char = self.scheme[rowi][coli]
                if char.isdigit():
                    number_str += char
                    if gear_adjacency_mask[rowi][coli]:
                        adjacent_to = gear_adjacency_mask[rowi][coli]
                else:
                    if number_str != "" and adjacent_to is not None:
                        parts[adjacent_to].append(int(number_str))
                    number_str = ""
                    adjacent_to = None
            # Check last number (if the last symbol in the row was a digit)
            if number_str != "" and adjacent_to is not None:
                parts[adjacent_to].append(int(number_str))

        return parts

    def get_gear_ratios(self):
        parts = self.get_gear_parts()
        total = 0
        for gear, two_parts in parts.items():
            if len(two_parts) != 2:
                print("Invalid parts", gear, two_parts, file=sys.stderr)
            total += two_parts[0] * two_parts[1]
        return total


class Day3(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.schematic = Schematic(list(self.filereader.lines()))
        self.star1_solution = 539590
        self.star2_solution = 80703636

    def star1(self):
        return self.schematic.sum_adjacent_numbers()

    def star2(self):
        return self.schematic.get_gear_ratios()
