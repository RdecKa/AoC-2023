import re
from aoclib.puzzle import Puzzle


edge_regex = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")


class Network:
    def __init__(self, instructions: str, edges: list[(str, str, str)]) -> None:
        self.name_map = {}
        self.node_count = 0
        self.a_node_idx = None
        self.z_node_idx = None

        self.instructions = [0 if c == "L" else 1 for c in instructions]

        self.edges = [None] * len(edges)
        for start, left, right in edges:
            start_idx = self.get_node_index(start)
            left_idx = self.get_node_index(left)
            right_idx = self.get_node_index(right)
            if self.edges[start_idx] is not None:
                raise AssertionError
            self.edges[start_idx] = (left_idx, right_idx)

    def get_node_index(self, node_name):
        """Map each node to an array index"""
        if node_name in self.name_map:
            return self.name_map[node_name]

        new_index = self.node_count
        self.name_map[node_name] = new_index

        if node_name == "AAA":
            self.a_node_idx = new_index
        elif node_name == "ZZZ":
            self.z_node_idx = new_index
        self.node_count += 1

        return new_index

    def count_step_to_z(self):
        current_node_idx = self.a_node_idx
        step_count = 0
        pc = 0
        while current_node_idx != self.z_node_idx:
            current_node_idx = self.edges[current_node_idx][self.instructions[pc]]
            step_count += 1
            pc += 1
            if pc >= len(self.instructions):
                pc = 0
        return step_count

    def __repr__(self) -> str:
        return f"""
{self.name_map} ({self.node_count} nodes)
AAA: {self.a_node_idx}, ZZZ: {self.z_node_idx}
instructions: {self.instructions}
edges: {self.edges}"""


def parse_network(lines):
    instructions = next(lines)
    next(lines)  # empty line
    edges = [edge_regex.match(line).groups() for line in lines]
    return Network(instructions, edges)


class Day8(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 12169
        self.star2_solution = None

    def star1(self):
        lines = self.filereader.lines()
        network = parse_network(lines)
        return network.count_step_to_z()

    def star2(self):
        return 0
