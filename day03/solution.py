from aoclib.grid import BoolGrid
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

    def get_adjacency_mask(self) -> BoolGrid:
        mask = BoolGrid(self.size(), self.size(), False)
        for rowi in range(self.size()):
            for coli in range(self.size()):
                if is_symbol(self.scheme[rowi][coli]):
                    mask.set_adjacent_9_fields(rowi, coli, True)
        return mask

    def sum_adjacent_numbers(self) -> int:
        adjacency_mask = self.get_adjacency_mask()
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


class Day3(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.schematic = Schematic(list(self.filereader.lines()))
        self.star1_solution = 539590
        self.star2_solution = None

    def star1(self):
        return self.schematic.sum_adjacent_numbers()

    def star2(self):
        return 0
