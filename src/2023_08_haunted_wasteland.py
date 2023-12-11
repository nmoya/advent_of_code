import math
from collections import deque
from dataclasses import dataclass

import utils


@dataclass
class Node:
    name: str
    left: str
    right: str

    def move(self, direction: int) -> str:
        if direction == 0:
            return self.left
        elif direction == 1:
            return self.right
        else:
            raise ValueError("Direction must be 0 or 1")


class HauntedMap:
    def __init__(self, filename):
        self.graph = {}
        self.instructions = []
        self._read_map(filename)

    def _read_map(self, filename):
        lines = list(utils.read_by_line(filename))
        self.instructions = lines[0]

        for line in lines[2:]:
            node = self.parse_line(line)
            self.graph[node.name] = node

    def parse_line(self, line) -> Node:
        name, neighbours = line.split("=")
        for char in ["(", ")", " "]:
            neighbours = neighbours.replace(char, "")
        left, right = neighbours.split(",")

        return Node(name.strip(), left.strip(), right.strip())

    def directions(self) -> int:
        # Left is 0, right is 1
        index = 0
        while True:
            if index == len(self.instructions):
                index = 0
            current = self.instructions[index]
            if current == "L":
                yield 0
            elif current == "R":
                yield 1
            index += 1

    def traverse(self, origin: str, destination: str):
        current = self.graph[origin]
        steps = 0
        for direction in self.directions():
            steps += 1
            current = self.graph[current.move(direction)]
            if current.name == destination:
                return steps
        return None

    def traverse_all_paths(self):
        queue = deque()
        next_queue = deque()
        steps = {}
        for node in self.graph.keys():
            if node.endswith("A"):
                queue.append((node, node))
                steps[node] = 0

        all_steps = 0
        for direction in self.directions():
            all_steps += 1
            while queue:
                origin, current_name = queue.popleft()
                current = self.graph[current_name]
                next = current.move(direction)
                if next.endswith("Z"):
                    steps[origin] = all_steps
                else:
                    next_queue.append((origin, next))
            if not next_queue:
                return math.lcm(*steps.values())
            queue = deque(next_queue)
            next_queue = deque()


def solution(filename):
    map = HauntedMap(filename)
    # print(map.traverse("AAA", "ZZZ"))

    print(map.traverse_all_paths())


def test_samples():
    map = HauntedMap("src/2023_08_haunted_wasteland_sample.txt")

    assert len(map.graph.keys()) == 7
    assert map.instructions == "RL"
    assert map.traverse("AAA", "ZZZ") == 2

    assert HauntedMap("src/2023_08_haunted_wasteland_sample_2.txt").traverse("AAA", "ZZZ") == 6
    assert HauntedMap("src/2023_08_haunted_wasteland_sample_3.txt").traverse_all_paths() == 6


if __name__ == "__main__":
    test_samples()
    solution("src/2023_08_haunted_wasteland.txt")
