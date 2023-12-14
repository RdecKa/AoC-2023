from aoclib.puzzle import Puzzle


ROUNDED = "O"
CUBE = "#"


def calculate_load(rows):
    last_blockers = [-1] * len(rows[0])
    max_load_single_rock = len(rows)
    total_load = 0
    for row_idx, row in enumerate(rows):
        for rock_idx, rock in enumerate(row):
            if rock == CUBE:
                last_blockers[rock_idx] = row_idx
            elif rock == ROUNDED:
                new_row_idx = last_blockers[rock_idx] + 1
                total_load += max_load_single_rock - new_row_idx
                last_blockers[rock_idx] += 1
    return total_load


class Day14(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 108857
        self.star2_solution = None

    def star1(self):
        rows = list(self.filereader.lines())
        return calculate_load(rows)

    def star2(self):
        return 0
