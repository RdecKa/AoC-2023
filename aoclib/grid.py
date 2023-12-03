class Grid:
    def __init__(self, width=0, height=0, default=False) -> None:
        self.width = width
        self.height = height
        self.grid = [[default for _ in range(width)] for _ in range(height)]

    def __getitem__(self, idx):
        return self.grid[idx]

    def __repr__(self) -> str:
        s = ""
        for row in self.grid:
            s += str(row) + "\n"
        return s


class BoolGrid(Grid):
    def __repr__(self) -> str:
        s = ""
        for row in self.grid:
            for element in row:
                s += "*" if element else "."
            s += "\n"
        return s

    def set_adjacent_9_fields(self, row, col, val):
        """Sets the field at (row, col) and its 8 adjacent fields to `val`"""
        for drow in range(-1, 2):
            for dcol in range(-1, 2):
                new_row = row + drow
                new_col = col + dcol
                if 0 <= new_row < self.height and 0 <= new_col < self.width:
                    self.grid[new_row][new_col] = val
