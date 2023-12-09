from aoclib.puzzle import Puzzle


def parse_input_line(line: str):
    return [int(x) for x in line.split(" ")]


def calculate_frontier(measured_values: list[int]) -> list[int]:
    """
    Returns the right-most entry in each row. This is all that is needed for
    extrapolating the next value.
    """
    frontier = []
    for val in measured_values:
        new_frontier = [val]
        for f in frontier:
            new_val = new_frontier[-1] - f
            if f == new_val == 0:
                break
            new_frontier.append(new_val)
        frontier = new_frontier
    return frontier


def extrapolate_next_day(measured_values: list[int]):
    return sum(calculate_frontier(measured_values))


class Day9(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 1992273652
        self.star2_solution = None

    def star1(self):
        histories = self.filereader.lines(parse_input_line)
        return sum(extrapolate_next_day(h) for h in histories)

    def star2(self):
        return 0
