from aoclib.grid import Grid
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
        self.clean_grid = Grid(len(lines[0]), len(lines), ".")
        self.loop_len = None

    def find_start_pose(self) -> Pose:
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

    def find_loop(self):
        """And save "clean" loop"""
        start_pose = self.find_start_pose()
        loop_length = 0
        pose = start_pose
        while (pose.row, pose.col) != (
            start_pose.row,
            start_pose.col,
        ) or loop_length == 0:
            pose = self.get_next_pose(pose)
            loop_length += 1
            self.clean_grid[pose.row][pose.col] = self.grid[pose.row][pose.col]
        self.loop_len = loop_length
        s = self.get_s_pipe_tile(start_pose.orientation, pose.orientation)
        self.clean_grid[start_pose.row][start_pose.col] = s

    def get_s_pipe_tile(
        self, start_orientation: Orientation, end_orientation: Orientation
    ) -> str:
        if start_orientation == end_orientation:
            if start_orientation in (Orientation.NORTH, Orientation.SOUTH):
                return "|"
            return "-"

        match start_orientation:
            case Orientation.NORTH:
                match end_orientation:
                    case Orientation.EAST:
                        return "J"
                    case Orientation.WEST:
                        return "L"
            case Orientation.SOUTH:
                match end_orientation:
                    case Orientation.EAST:
                        return "7"
                    case Orientation.WEST:
                        return "F"
            case Orientation.EAST:
                match end_orientation:
                    case Orientation.NORTH:
                        return "F"
                    case Orientation.SOUTH:
                        return "L"
            case Orientation.WEST:
                match end_orientation:
                    case Orientation.NORTH:
                        return "7"
                    case Orientation.SOUTH:
                        return "J"
        raise AssertionError

    def print_clean_loop(self):
        for row in self.clean_grid:
            print("".join(row))

    def count_enclosed_fields_in_row(self, row: list[str]):
        total = 0
        in_loop = False
        border_enter_orientation = None
        for field in row:
            match field:
                case ".":
                    if in_loop:
                        total += 1
                case "-":
                    continue
                case "|":
                    in_loop = not in_loop
                case "L":
                    border_enter_orientation = Orientation.NORTH
                case "F":
                    border_enter_orientation = Orientation.SOUTH
                case "J":
                    if border_enter_orientation == Orientation.SOUTH:
                        in_loop = not in_loop
                    border_enter_orientation = None
                case "7":
                    if border_enter_orientation == Orientation.NORTH:
                        in_loop = not in_loop
                    border_enter_orientation = None
        return total

    def count_enclosed_fields(self):
        return sum(self.count_enclosed_fields_in_row(row) for row in self.clean_grid)


class Day10(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

        lines = self.filereader.lines()
        self.pipe_map = PipeMap(list(lines))
        self.pipe_map.find_loop()

        self.star1_solution = 6820
        self.star2_solution = 337

    def star1(self):
        return self.pipe_map.loop_len // 2

    def star2(self):
        # If we cross the loop one/three/five times, we're in the loop.
        # If we cross the loop two/four/six times, we're outside the loop.
        return self.pipe_map.count_enclosed_fields()
