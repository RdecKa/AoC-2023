from aoclib.filereader import FileReader


class Puzzle:
    """AoC solution for one day"""

    def __init__(self, filename):
        self.filereader = FileReader(filename)
        self.star1_solution = None
        self.star2_solution = None

    def star1(self):
        """Star 1 solution"""
        raise NotImplementedError

    def star2(self):
        """Star 2 solution"""
        raise NotImplementedError

    def test_star1(self):
        """Test star 1"""
        return self.star1() == self.star1_solution

    def test_star2(self):
        """Test star 2"""
        return self.star2() == self.star2_solution
