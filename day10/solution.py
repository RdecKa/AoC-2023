from aoclib.puzzle import Puzzle
from enum import Enum


class Orientation(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)


class Pose:
    def __init__(self, row: int, col: int, orientation: Orientation) -> None:
        self.row = row
        self.col = col
        self.orientation = orientation

    def __repr__(self) -> str:
        return f"({self.row}, {self.col}, {self.orientation})"

    def __iter__(self):
        return iter((self.row, self.col, self.orientation))

    def __getitem__(self, key):
        match key:
            case 0:
                return self.row
            case 1:
                return self.col
            case 2:
                return self.orientation


class PipeMap:
    def __init__(self, lines: list[str]) -> None:
        self.grid = lines

    def find_start_pose(self) -> tuple[int, int]:
        for i, row in enumerate(self.grid):
            start_col = row.find("S")
            if start_col > -1:
                start_row = i
                break

        if start_row > 0 and self.grid[start_row - 1][start_col] in ("|", "7", "F"):
            orientation = Orientation.NORTH
        elif start_col > 0 and self.grid[start_row][start_col - 1] in ("-", "F", "L"):
            orientation = Orientation.WEST
        else:
            # North and west are blocked, so the loop goes to the south and to the east.
            orientation = Orientation.SOUTH
        return Pose(start_row, start_col, orientation)

    def get_next_pose(self, current_pose: Pose):
        current_row, current_col, orientation = current_pose
        new_row = current_row + orientation.value[0]
        new_col = current_col + orientation.value[1]
        new_orientation = self.get_next_orientation(
            self.grid[new_row][new_col], orientation
        )
        return Pose(new_row, new_col, new_orientation)

    def get_next_orientation(self, pipe_tile: str, current_orientation: Orientation):
        if pipe_tile == "S":
            return current_orientation
        match current_orientation:
            case Orientation.NORTH:
                match pipe_tile:
                    case "|":
                        return Orientation.NORTH
                    case "7":
                        return Orientation.WEST
                    case "F":
                        return Orientation.EAST
            case Orientation.SOUTH:
                match pipe_tile:
                    case "|":
                        return Orientation.SOUTH
                    case "L":
                        return Orientation.EAST
                    case "J":
                        return Orientation.WEST
            case Orientation.EAST:
                match pipe_tile:
                    case "-":
                        return Orientation.EAST
                    case "J":
                        return Orientation.NORTH
                    case "7":
                        return Orientation.SOUTH
            case Orientation.WEST:
                match pipe_tile:
                    case "-":
                        return Orientation.WEST
                    case "L":
                        return Orientation.NORTH
                    case "F":
                        return Orientation.SOUTH
        print(pipe_tile, current_orientation)
        raise AssertionError

    def find_loop_length(self):
        start_pose = self.find_start_pose()
        loop_length = 0
        pose = start_pose
        while (pose[0], pose[1]) != (start_pose[0], start_pose[1]) or loop_length == 0:
            pose = self.get_next_pose(pose)
            loop_length += 1
        return loop_length


class Day10(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 6820
        self.star2_solution = None

    def star1(self):
        lines = self.filereader.lines()
        pipe_map = PipeMap(list(lines))
        return pipe_map.find_loop_length() // 2

    def star2(self):
        return 0
