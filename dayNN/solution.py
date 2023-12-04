from aoclib.puzzle import Puzzle


class DayNN(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = None
        self.star2_solution = None

    def star1(self):
        return 0

    def star2(self):
        return 0
