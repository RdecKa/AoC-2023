from operator import itemgetter
from aoclib.puzzle import Puzzle


ROUNDED = "O"
CUBE = "#"


def calculate_load(rows):
    last_blockers = [-1] * len(rows[0])
    max_load_single_rock = len(rows)
    total_load = 0
    for row_idx, row in enumerate(rows):
        for col_idx, rock in enumerate(row):
            if rock == CUBE:
                last_blockers[col_idx] = row_idx
            elif rock == ROUNDED:
                new_row_idx = last_blockers[col_idx] + 1
                total_load += max_load_single_rock - new_row_idx
                last_blockers[col_idx] += 1
    return total_load


class Platform:
    def __init__(self, rows: list[str]) -> None:
        self.num_rows = len(rows)
        self.num_cols = len(rows[0])
        self.rocks = []
        self.parse_grid(rows)

    def parse_grid(self, rows: list[str]):
        for row_idx, row in enumerate(rows):
            for col_idx, rock_type in enumerate(row):
                if rock_type in (CUBE, ROUNDED):
                    self.rocks.append((row_idx, col_idx, rock_type))

    def calculate_north_load(self):
        max_load_single_rock = self.num_rows
        load = 0
        for row_idx, _, rock_type in self.rocks:
            if rock_type == ROUNDED:
                load += max_load_single_rock - row_idx
        return load

    def turn_north(self):
        # Sort by row (0) for north and south
        # Sort by col (1) for west and east
        rocks = sorted(self.rocks, key=itemgetter(0), reverse=False)
        last_blockers = [-1] * self.num_cols
        for rock_idx, (row_idx, col_idx, rock_type) in enumerate(rocks):
            if rock_type == CUBE:
                last_blockers[col_idx] = row_idx
            elif rock_type == ROUNDED:
                new_row_idx = last_blockers[col_idx] + 1
                rocks[rock_idx] = (new_row_idx, col_idx, rock_type)
                last_blockers[col_idx] += 1
        self.rocks = rocks


class Day14(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        rows = list(self.filereader.lines())
        self.platform = Platform(rows)

        self.star1_solution = 108857
        self.star2_solution = None

    def star1(self):
        self.platform.turn_north()
        return self.platform.calculate_north_load()

    def star2(self):
        return 0
