import re
from aoclib.puzzle import Puzzle


class Set:
    def __init__(self) -> None:
        self.red = 0
        self.green = 0
        self.blue = 0

    def __repr__(self) -> str:
        return f"(r: {self.red}, g: {self.green}, b: {self.blue})"


class Game:
    def __init__(self, game_id, sets) -> None:
        self.game_id = game_id
        self.sets = sets

    def __repr__(self) -> str:
        return f"Game {self.game_id}: {self.sets}"


game_regex = re.compile("Game ([0-9]+): ")
set_regex = re.compile("((?:[0-9]+ (?:(?:red|green|blue),? ?))+)")
ball_regex = re.compile("([0-9]+) (red|green|blue)")


def create_set(set_string: str):
    s = Set()
    parsed = ball_regex.findall(set_string)
    for count, color in parsed:
        count = int(count)
        match color:
            case "red":
                s.red = count
            case "green":
                s.green = count
            case "blue":
                s.blue = count
    return s


def parse_game_from_input_line(line: str):
    game_id = int(game_regex.search(line).group(1))
    sets = [create_set(s) for s in set_regex.findall(line)]
    return Game(game_id, sets)


def is_game_valid(game: Game):
    limit_red = 12
    limit_green = 13
    limit_blue = 14
    for s in game.sets:
        if s.red > limit_red or s.green > limit_green or s.blue > limit_blue:
            return False
    return True


def get_game_power(game: Game):
    red = max(s.red for s in game.sets)
    green = max(s.green for s in game.sets)
    blue = max(s.blue for s in game.sets)
    return red * green * blue


class Day2(Puzzle):
    def star1(self):
        games = self.filereader.lines(parse_game_from_input_line)
        total = 0
        for game in games:
            if is_game_valid(game):
                total += game.game_id
        return total

    def star2(self):
        games = self.filereader.lines(parse_game_from_input_line)
        return sum(get_game_power(g) for g in games)
