import math
import re
from aoclib.puzzle import Puzzle


edge_regex = re.compile(r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)")


class Network:
    def __init__(self, instructions: str, edges: list[(str, str, str)]) -> None:
        self.name_map = {}
        self.node_count = 0
        self.a_nodes_idx = []
        self.z_nodes_idx = set()

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

        new_idx = self.node_count
        self.name_map[node_name] = new_idx

        self.handle_special_nodes(node_name, new_idx)
        self.node_count += 1

        return new_idx

    def handle_special_nodes(self, node_name, new_idx):
        return NotImplementedError

    def count_step_to_z(self):
        current_node_idx = self.a_nodes_idx[0]
        final_node = self.z_nodes_idx.pop()
        step_count = 0
        pc = 0
        while current_node_idx != final_node:
            current_node_idx = self.edges[current_node_idx][self.instructions[pc]]
            step_count += 1
            pc += 1
            if pc >= len(self.instructions):
                pc = 0
        return step_count

    def get_cycle_info(self, start_node_idx):
        visited = [
            [None for i in range(len(self.instructions))]
            for n in range(self.node_count)
        ]
        current_node_idx = start_node_idx
        step_count = 0
        pc = 0
        z_locations = []
        while not visited[current_node_idx][pc]:
            visited[current_node_idx][pc] = step_count
            current_node_idx = self.edges[current_node_idx][self.instructions[pc]]

            step_count += 1

            if current_node_idx in self.z_nodes_idx:
                # Observation: Every cycle has only one Z node (except in input3),
                # and it always appears at the end of the cycle
                z_locations.append(step_count)

            pc += 1
            if pc >= len(self.instructions):
                pc = 0
        cycle_start = visited[current_node_idx][pc]
        return (cycle_start, step_count - cycle_start, z_locations)

    def __repr__(self) -> str:
        return f"""
{self.name_map} ({self.node_count} nodes)
AAA: {self.a_nodes_idx}, ZZZ: {self.z_nodes_idx}
instructions: {self.instructions}
edges: {self.edges}"""


class HumanNetwork(Network):
    def handle_special_nodes(self, node_name: str, new_idx: int):
        if node_name == "AAA":
            self.a_nodes_idx = [new_idx]
        elif node_name == "ZZZ":
            self.z_nodes_idx = {new_idx}


class GhostNetwork(Network):
    def handle_special_nodes(self, node_name: str, new_idx: int):
        if node_name.endswith("A"):
            self.a_nodes_idx.append(new_idx)
        elif node_name.endswith("Z"):
            self.z_nodes_idx.add(new_idx)


def parse_network(lines, network_type):
    instructions = next(lines)
    next(lines)  # empty line
    edges = [edge_regex.match(line).groups() for line in lines]
    return network_type(instructions, edges)


class Day8(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.star1_solution = 12169
        self.star2_solution = 12030780859469

    def star1(self):
        lines = self.filereader.lines()
        network = parse_network(lines, HumanNetwork)
        return network.count_step_to_z()

    def star2(self):
        lines = self.filereader.lines()
        network = parse_network(lines, GhostNetwork)
        z_locations = []
        for a_node in network.a_nodes_idx:
            # Observation: every cycle has exactly one Z node. This node appears
            # after step N, 2N, 3N ...
            _, _, z_loc = network.get_cycle_info(a_node)
            # take the last entry to make it work for input3
            z_locations.append(z_loc[-1])

        return math.lcm(*z_locations)
