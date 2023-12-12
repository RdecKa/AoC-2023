from aoclib.puzzle import Puzzle

OPERATIONAL = "."
DEFECT = "#"
UNKNOWN = "?"


def parse_input_line(line: str):
    spring_row, groups_str = line.split(" ")
    groups = [int(g) for g in groups_str.split(",")]
    return spring_row, groups


def count_possible_configurations(row: str, start_pos: int, groups: list[int]):
    if len(groups) == 0:
        for spring in row[start_pos:]:
            if spring == DEFECT:
                return 0
        return 1
    if start_pos >= len(row):
        # len(groups) > 0 ==> not possible
        return 0

    if row[start_pos] == OPERATIONAL:
        return count_possible_configurations(row, start_pos + 1, groups)
    if row[start_pos] == DEFECT:
        contiguous = groups[0]
        end_pos = start_pos + contiguous - 1
        if end_pos >= len(row):
            return 0
        for spring in row[start_pos + 1 : end_pos + 1]:
            if spring == OPERATIONAL:
                # All springs should be either defect or unknown
                return 0
        if end_pos == len(row) - 1:
            # Group ending at the end of the row
            return count_possible_configurations(
                row, start_pos + contiguous, groups[1:]
            )
        # Defected groups must be separated by at least one operating spring
        if row[end_pos + 1] == OPERATIONAL:
            return count_possible_configurations(
                row, start_pos + contiguous, groups[1:]
            )
        if row[end_pos + 1] == DEFECT:
            return 0
        row = row[: end_pos + 1] + OPERATIONAL + row[end_pos + 1 + 1 :]
        return count_possible_configurations(row, start_pos + contiguous, groups[1:])
    # row[start_pos] == UNKNOWN
    row_operational = row[:start_pos] + OPERATIONAL + row[start_pos + 1 :]
    count_if_operational = count_possible_configurations(
        row_operational, start_pos, groups
    )
    row_defect = row[:start_pos] + DEFECT + row[start_pos + 1 :]
    count_if_defect = count_possible_configurations(row_defect, start_pos, groups)
    return count_if_operational + count_if_defect


class Day12(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 7169
        self.star2_solution = None

    def star1(self):
        rows = self.filereader.lines(parse_input_line)
        total = 0
        for row, groups in rows:
            total += count_possible_configurations(row, 0, groups)
        return total

    def star2(self):
        return 0
