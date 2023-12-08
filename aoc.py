import argparse
import os.path
import sys

from day01.solution import Day1
from day02.solution import Day2
from day03.solution import Day3
from day04.solution import Day4
from day05.solution import Day5
from day06.solution import Day6
from day07.solution import Day7
from day08.solution import Day8


parser = argparse.ArgumentParser(
    prog="AoC Solutions", description="Solutions for Advent of Code Puzzles"
)
parser.add_argument("-d", "--day", type=int, help="select AoC puzzle to run")
parser.add_argument(
    "-i",
    "--input",
    type=int,
    help="select input file (leave empty or set to 0 for non-test puzzle input)",
)
parser.add_argument("-s", "--star", type=int, help="select star (leave empty for both)")
parser.add_argument("-t", "--test", type=bool, help="test all puzzles")

args = parser.parse_args()


solutions = [None, Day1, Day2, Day3, Day4, Day5, Day6, Day7, Day8]
if args.test:

    def report(star, success):
        return f"Star {star}: {'success' if success else 'fail'}"

    for i in range(1, len(solutions)):
        solution = solutions[i](f"day{i:02}/input.txt")
        success1 = solution.test_star1()
        success2 = solution.test_star2()

        print(f"[Day {i}] {report(1, success1)}, {report(2, success2)}")
    sys.exit(0)


suffix = f"-{args.input}" if args.input else ""
filename = f"day{args.day:02}/input{suffix}.txt"
if not os.path.isfile(filename):
    print(f"File '{filename}' does not exist", file=sys.stderr)
    sys.exit(1)

if 1 <= args.day < len(solutions):
    puzzle = solutions[args.day](filename)
else:
    print(f"No solution for day '{args.day}'", file=sys.stderr)
    sys.exit(1)

if args.star is None or args.star == 1:
    print(puzzle.star1())
if args.star is None or args.star == 2:
    print(puzzle.star2())
