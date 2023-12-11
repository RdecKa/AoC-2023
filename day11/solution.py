from aoclib.puzzle import Puzzle


class Position:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

    def __repr__(self) -> str:
        return f"({self.row}, {self.col})"

    def __iter__(self):
        return iter((self.row, self.col))


def count_smaller_values(values: list, smaller_than: int):
    return sum(1 for v in values if v < smaller_than)


def manhattan_distance(p1: Position, p2: Position):
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)


class Universe:
    def __init__(self) -> None:
        self.galaxy_locations: list[Position] = []
        # Empty rows and cols in the original input
        self.empty_rows = []
        self.empty_cols = []
        self.expanded_galaxy_locations: list[Position] = []

    def add_galaxy(self, row, col):
        self.galaxy_locations.append(Position(row, col))

    def mark_empty_row(self, row):
        self.empty_rows.append(row)

    def mark_empty_col(self, col):
        self.empty_cols.append(col)

    def __repr__(self) -> str:
        return (
            f"{self.galaxy_locations}\n"
            + f"Empty rows: {self.empty_rows}\n"
            + f"Empty cols: {self.empty_cols}\n"
            + f"Expanded: {self.expanded_galaxy_locations}"
        )

    def expand(self):
        for original_row, original_col in self.galaxy_locations:
            # Count number of smaller rows/cols that are empty
            smaller_rows = count_smaller_values(self.empty_rows, original_row)
            smaller_cols = count_smaller_values(self.empty_cols, original_col)
            self.expanded_galaxy_locations.append(
                Position(original_row + smaller_rows, original_col + smaller_cols)
            )

    def sum_expanded_distances(self):
        total = 0
        for p1 in self.expanded_galaxy_locations:
            for p2 in self.expanded_galaxy_locations:
                if p1 == p2:
                    continue
                total += manhattan_distance(p1, p2)
        return total // 2


def parse_input(lines):
    """Create a spares matrix and mark empty rows and cols"""
    universe = Universe()
    empty_cols = []
    for row_idx, line in enumerate(lines):
        if row_idx == 0:
            empty_cols = [True for _ in range(len(line))]
        row_empty = True
        for col_idx, el in enumerate(line):
            if el == "#":
                universe.add_galaxy(row_idx, col_idx)
                empty_cols[col_idx] = False
                row_empty = False
        if row_empty:
            universe.mark_empty_row(row_idx)
    for col_idx, empty in enumerate(empty_cols):
        if empty:
            universe.mark_empty_col(col_idx)
    return universe


class Day11(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 9734203
        self.star2_solution = None

    def star1(self):
        universe = parse_input(self.filereader.lines())
        universe.expand()
        return universe.sum_expanded_distances()

    def star2(self):
        return 0
