import argparse
import os.path
import sys

from day01.solution import Day1


parser = argparse.ArgumentParser(
    prog="AoC Solutions", description="Solutions for Advent of Code Puzzles"
)
parser.add_argument(
    "-d", "--day", type=int, required=True, help="select AoC puzzle to run"
)
parser.add_argument(
    "-i",
    "--input",
    type=int,
    help="select input file (leave empty or set to 0 for non-test puzzle input)",
)
parser.add_argument("-s", "--star", type=int, help="select star (leave empty for both)")

args = parser.parse_args()

suffix = f"-{args.input}" if args.input else ""
filename = f"day{args.day:02}/input{suffix}.txt"
if not os.path.isfile(filename):
    print(f"File '{filename}' does not exist", file=sys.stderr)
    sys.exit(1)

match args.day:
    case 1:
        puzzle = Day1(filename)
    case _:
        print(f"No solution for day '{args.day}'", file=sys.stderr)
        sys.exit(1)

if args.star is None or args.star == 1:
    print(puzzle.star1())
if args.star is None or args.star == 2:
    print(puzzle.star2())
