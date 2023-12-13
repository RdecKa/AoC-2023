from aoclib.puzzle import Puzzle

OPERATIONAL = "."
DEFECT = "#"
UNKNOWN = "?"

# Cleared after processing every row
memo = {}


def parse_input_line(line: str):
    spring_row, groups_str = line.split(" ")
    groups = [int(g) for g in groups_str.split(",")]
    return spring_row, groups


def parse_folded_input_line(line: str):
    folded_spring_row, folded_groups_str = line.split(" ")
    spring_row = "?".join([folded_spring_row] * 5)
    groups_str = ",".join([folded_groups_str] * 5)
    groups = [int(g) for g in groups_str.split(",")]
    return spring_row, groups


def handle_defect_group(row: str, start_pos: int, groups: list[int]):
    contiguous = groups[0]
    end_pos = start_pos + contiguous - 1
    if end_pos >= len(row):
        return 0
    for spring in row[start_pos + 1 : end_pos + 1]:
        if spring == OPERATIONAL:
            # All springs should be either defect or unknown
            return 0
    if end_pos == len(row) - 1:
        # Group is ending at the end of the row
        if len(groups) == 1:
            return 1
        return 0
    # Defected groups must be separated by at least one operating spring
    if row[end_pos + 1] == DEFECT:
        return 0
    return count_possible_configurations(row, end_pos + 2, groups[1:])


def count_possible_configurations(row: str, start_pos: int, groups: list[int]):
    memo_key = (start_pos, len(groups))
    if memo_key in memo:
        return memo[memo_key]
    if len(groups) == 0:
        for spring in row[start_pos:]:
            if spring == DEFECT:
                return 0
        return 1
    if start_pos >= len(row):
        # len(groups) > 0 ==> not possible
        return 0
    remaining_space = len(row) - start_pos
    needed_space = sum(groups) + len(groups) - 1
    if remaining_space < needed_space:
        return 0

    if row[start_pos] == OPERATIONAL:
        # Jump over all operational spring
        skip = 1
        while start_pos + skip < len(row) and row[start_pos + skip] == OPERATIONAL:
            skip += 1
        return count_possible_configurations(row, start_pos + skip, groups)
    if row[start_pos] == DEFECT:
        return handle_defect_group(row, start_pos, groups)

    # row[start_pos] == UNKNOWN
    count_if_operational = count_possible_configurations(row, start_pos + 1, groups)
    count_if_defect = handle_defect_group(row, start_pos, groups)
    result = count_if_operational + count_if_defect
    memo[memo_key] = result
    return result


class Day12(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 7169
        self.star2_solution = 1738259948652

    def star1(self):
        global memo
        rows = self.filereader.lines(parse_input_line)
        total = 0
        for row, groups in rows:
            memo = {}
            total += count_possible_configurations(row, 0, groups)
        return total

    def star2(self):
        global memo
        rows = self.filereader.lines(parse_folded_input_line)
        total = 0
        for row, groups in rows:
            memo = {}
            total += count_possible_configurations(row, 0, groups)
        return total
