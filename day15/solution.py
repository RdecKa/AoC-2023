from aoclib.puzzle import Puzzle


def get_step_hash(step: str):
    current = 0
    for c in step:
        current += ord(c)
        current *= 17
        current &= 255
    return current


class Day15(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 518107
        self.star2_solution = None

    def star1(self):
        manual = next(self.filereader.lines())
        steps = manual.split(",")
        return sum(get_step_hash(step) for step in steps)

    def star2(self):
        return 0
