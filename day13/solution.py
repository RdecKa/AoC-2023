from aoclib.puzzle import Puzzle


def transpose(pattern: list[str]):
    new_pattern = [""] * len(pattern[0])
    for row in pattern:
        for i, el in enumerate(row):
            new_pattern[i] += el
    return new_pattern


def parse_input(lines):
    patterns = []
    new_pattern = []
    for line in lines:
        if line == "":
            patterns.append(new_pattern)
            new_pattern = []
        else:
            new_pattern.append(line)
    patterns.append(new_pattern)
    return patterns


def check_vertical_reflection(pattern: list[str], first_repeated_line: int):
    """Along a horizontal reflection line"""
    row_count = len(pattern)
    for i in range(min(first_repeated_line, row_count - first_repeated_line)):
        if pattern[first_repeated_line - 1 - i] != pattern[first_repeated_line + i]:
            return None
    return first_repeated_line - 1 + 1


def find_horizontal_reflection(pattern: list[str]):
    """Along a vertical reflection line"""
    transposed = transpose(pattern)
    return find_vertical_reflection(transposed)


def find_vertical_reflection(pattern: list[str]):
    seen = {}
    for i, row in enumerate(pattern):
        if row in seen:
            reflection = check_vertical_reflection(pattern, i)
            if not reflection is None:
                return reflection
            seen[row] = i
        else:
            seen[row] = i
    return None


class Day13(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 42974
        self.star2_solution = None

    def star1(self):
        patterns = parse_input(self.filereader.lines())
        total = 0
        for pattern in patterns:
            vertical = find_vertical_reflection(pattern)
            if vertical:
                total += 100 * vertical
            else:
                horizontal = find_horizontal_reflection(pattern)
                total += horizontal
        return total

    def star2(self):
        return 0
