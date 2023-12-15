from collections import OrderedDict
import re
from aoclib.puzzle import Puzzle

add_regex = re.compile(r"(.+)=([1-9])")
remove_regex = re.compile(r"(.+)-")


def get_hash(original: str):
    current = 0
    for c in original:
        current += ord(c)
        current *= 17
        current &= 255
    return current


class Lens:
    def __init__(self, step: str) -> None:
        add = add_regex.match(step)
        if add:
            self.label = add.group(1)
            self.value = int(add.group(2))
        else:
            self.label = remove_regex.match(step).group(1)
            self.value = None
        self.step_hash = get_hash(self.label)

    def __repr__(self):
        return f"({self.label},{self.value})"


class Box:
    def __init__(self, i: int) -> None:
        self.ordered_map = OrderedDict()
        self.index = i

    def __repr__(self) -> str:
        return f"{self.ordered_map}"

    def update_or_add(self, lens: Lens):
        self.ordered_map[lens.label] = lens.value

    def remove(self, lens: Lens):
        self.ordered_map.pop(lens.label, None)

    def focusing_power(self) -> int:
        return (1 + self.index) * sum(
            (slot_idx + 1) * focal_length
            for slot_idx, (_, focal_length) in enumerate(self.ordered_map.items())
        )


class Hashmap:
    def __init__(self) -> None:
        self.boxes = [None] * 256
        for i, _ in enumerate(self.boxes):
            self.boxes[i] = Box(i)

    def __repr__(self) -> str:
        result = ""
        for i, box in enumerate(self.boxes):
            if len(box.ordered_map) > 0:
                result += f"{i}: {box}\n"
        return result

    def execute_step(self, step):
        lens = Lens(step)
        if lens.value:
            self.boxes[lens.step_hash].update_or_add(lens)
        else:
            self.boxes[lens.step_hash].remove(lens)

    def focusing_power(self) -> int:
        return sum(box.focusing_power() for box in self.boxes)


class Day15(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

        manual = next(self.filereader.lines())
        self.steps = manual.split(",")

        self.star1_solution = 518107
        self.star2_solution = 303404

    def star1(self):
        return sum(get_hash(step) for step in self.steps)

    def star2(self):
        hashmap = Hashmap()
        for step in self.steps:
            hashmap.execute_step(step)
        return hashmap.focusing_power()
