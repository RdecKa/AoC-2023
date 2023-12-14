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
        # Store seen configurations because they repeat themselves
        self.seen_configurations = {}

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

    def turn_north_or_south(self, north: bool):
        # Sort by row (0) for north and south
        if north:
            self.rocks.sort(key=itemgetter(0), reverse=False)
            last_blockers = [-1] * self.num_cols
        else:
            self.rocks.sort(key=itemgetter(0), reverse=True)
            last_blockers = [self.num_rows] * self.num_cols

        for rock_idx, (row_idx, col_idx, rock_type) in enumerate(self.rocks):
            if rock_type == CUBE:
                last_blockers[col_idx] = row_idx
            elif rock_type == ROUNDED:
                if north:
                    new_row_idx = last_blockers[col_idx] + 1
                else:
                    new_row_idx = last_blockers[col_idx] - 1
                self.rocks[rock_idx] = (new_row_idx, col_idx, rock_type)
                last_blockers[col_idx] = new_row_idx

    def turn_west_or_east(self, west: bool):
        # Sort by col (1) for west and east
        if west:
            self.rocks.sort(key=itemgetter(1), reverse=False)
            last_blockers = [-1] * self.num_rows
        else:
            self.rocks.sort(key=itemgetter(1), reverse=True)
            last_blockers = [self.num_cols] * self.num_rows

        for rock_idx, (row_idx, col_idx, rock_type) in enumerate(self.rocks):
            if rock_type == CUBE:
                last_blockers[row_idx] = col_idx
            elif rock_type == ROUNDED:
                if west:
                    new_col_idx = last_blockers[row_idx] + 1
                else:
                    new_col_idx = last_blockers[row_idx] - 1
                self.rocks[rock_idx] = (row_idx, new_col_idx, rock_type)
                last_blockers[row_idx] = new_col_idx

    def perform_cycle(self):
        self.turn_north_or_south(north=True)
        self.turn_west_or_east(west=True)
        self.turn_north_or_south(north=False)
        self.turn_west_or_east(west=False)

    def perform_cycles(self, n):
        i = 0
        while i < n:
            self.perform_cycle()
            key = tuple((row, col) for row, col, type in self.rocks if type == ROUNDED)
            if key in self.seen_configurations:
                step = i - self.seen_configurations[key]
                break
            self.seen_configurations[key] = i
            i += 1
        remaining_cycles = n - i
        remaining_after_skipped_cycles = remaining_cycles % step
        for _ in range(remaining_after_skipped_cycles - 1):
            self.perform_cycle()


class Day14(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.rows = list(self.filereader.lines())

        self.star1_solution = 108857
        self.star2_solution = 95273

    def star1(self):
        platform = Platform(self.rows)
        platform.turn_north_or_south(north=True)
        return platform.calculate_north_load()

    def star2(self):
        platform = Platform(self.rows)
        platform.perform_cycles(1000000000)
        return platform.calculate_north_load()
