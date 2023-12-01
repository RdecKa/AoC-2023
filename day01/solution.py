import re
from aoclib.puzzle import Puzzle


to_digit = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_line_value(line, digit_pattern):
    digit = re.compile("(" + digit_pattern + ")")
    matches = digit.findall(line)
    combined = to_digit[matches[0]] + to_digit[matches[-1]]
    return int(combined)


class Day1(Puzzle):
    def star1(self):
        digit_pattern = "[1-9]"
        return sum(
            self.filereader.lines(lambda line: get_line_value(line, digit_pattern))
        )

    def star2(self):
        # "?=" added to capture overlapping words, like "twone"
        digit_pattern = "?=([1-9]|one|two|three|four|five|six|seven|eight|nine)"
        return sum(
            self.filereader.lines(lambda line: get_line_value(line, digit_pattern))
        )
