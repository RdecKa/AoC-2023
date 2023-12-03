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

    def set(self, row, col, val):
        """Sets (row, col) to val if both indices are valid"""
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = val

    def modify(self, row, col, func):
        """Sets (row, col) to func(old_value) if both indices are valid"""
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = func(self.grid[row][col])

    def set_adjacent_9_fields(self, row, col, val):
        """Sets the field at (row, col) and its 8 adjacent fields to `val`"""
        for drow in range(-1, 2):
            for dcol in range(-1, 2):
                self.set(row + drow, col + dcol, val)


class BoolGrid(Grid):
    def __repr__(self) -> str:
        s = ""
        for row in self.grid:
            for element in row:
                s += "*" if element else "."
            s += "\n"
        return s


class IntGrid(Grid):
    def __repr__(self) -> str:
        s = ""
        for row in self.grid:
            for element in row:
                s += f"{element: <3}"
            s += "\n"
        return s
