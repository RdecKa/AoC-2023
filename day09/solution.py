from aoclib.puzzle import Puzzle


def parse_input_line(line: str):
    return [int(x) for x in line.split(" ")]


def calculate_frontier(measured_values: list[int], reverse_time: bool) -> list[int]:
    """
    Returns the right-most (left-most when time reversed) entry in each row.
    This is all that is needed for extrapolating the next value.
    """
    if reverse_time:
        measured_values.reverse()
    frontier = []
    for val in measured_values:
        new_frontier = [val]
        for f in frontier:
            if reverse_time:
                new_val = f - new_frontier[-1]
            else:
                new_val = new_frontier[-1] - f
            new_frontier.append(new_val)
        frontier = new_frontier
    return frontier


def extrapolate_next_day(measured_values: list[int]):
    frontier = calculate_frontier(measured_values, False)
    return sum(frontier)


def extrapolate_previous_day(measured_values: list[int]):
    frontier = calculate_frontier(measured_values, True)
    val = 0
    for v in reversed(frontier):
        val = v - val
    return val


class Day9(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 1992273652
        self.star2_solution = 1012

    def star1(self):
        histories = self.filereader.lines(parse_input_line)
        return sum(extrapolate_next_day(h) for h in histories)

    def star2(self):
        histories = self.filereader.lines(parse_input_line)
        return sum(extrapolate_previous_day(h) for h in histories)
