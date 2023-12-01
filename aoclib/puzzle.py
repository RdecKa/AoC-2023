from aoclib.filereader import FileReader


class Puzzle:
    """AoC solution for one day"""

    def __init__(self, filename):
        self.filereader = FileReader(filename)

    def star1(self):
        """Star 1 solution"""
        raise NotImplementedError

    def star2(self):
        """Star 2 solution"""
        raise NotImplementedError
