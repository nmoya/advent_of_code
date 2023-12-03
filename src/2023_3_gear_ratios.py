from dataclasses import dataclass
from typing import List, Tuple

import utils


@dataclass
class Coordinate:
    line: int
    column: int

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Coordinate):
            return NotImplemented
        return self.line == __value.line and self.column == __value.column

    def __hash__(self) -> int:
        return hash((self.line, self.column))


@dataclass
class NumberNode:
    id: str
    number: int
    line_number: int
    col_start: int
    col_end: int
    line_text: str

    def coordinates(self) -> List[Coordinate]:
        for column in range(self.col_start, self.col_end):
            yield Coordinate(self.line_number, column)


@dataclass
class GearNode:
    id: str
    line: int
    column: int
    adjacent_numbers: List[NumberNode]

    def gear_ratio(self) -> int:
        if len(self.adjacent_numbers) != 2:
            return 0
        return self.adjacent_numbers[0].number * self.adjacent_numbers[1].number


@dataclass
class Matrix:
    matrix: List[str]
    nodes: List[NumberNode]
    gears: List[GearNode]

    def gear_by_coord(self, coord: Coordinate) -> GearNode | None:
        for gear in self.gears:
            if gear.id == gear_id(coord.line, coord.column):
                return gear
        return None

    def num_lines(self) -> int:
        return len(self.matrix)

    def num_colmns(self) -> int:
        return len(self.matrix[0])

    def valid_coordinates(self, coordinate: Coordinate) -> bool:
        line, column = coordinate.line, coordinate.column
        return line >= 0 and line < self.num_lines() and column >= 0 and column < self.num_colmns()

    def adjacent8_coordinates(self, coordinate: Coordinate) -> List[Coordinate]:
        line, column = coordinate.line, coordinate.column
        all_coordinates = [
            Coordinate(line - 1, column - 1),
            Coordinate(line - 1, column),
            Coordinate(line - 1, column + 1),
            Coordinate(line, column - 1),
            Coordinate(line, column + 1),
            Coordinate(line + 1, column - 1),
            Coordinate(line + 1, column),
            Coordinate(line + 1, column + 1),
        ]
        return [c for c in all_coordinates if self.valid_coordinates(c)]

    def is_part_digit(self, coord: Coordinate) -> bool:
        char = self.matrix[coord.line][coord.column]
        return not char.isdigit() and not char == "."

    def is_adjacent_to_gear(self, coord: Coordinate) -> bool:
        char = self.matrix[coord.line][coord.column]
        return char == "*"

    def node_adjacents(self, node: NumberNode) -> List[Coordinate]:
        node_adjacents = set()
        for coord in node.coordinates():
            node_adjacents = node_adjacents.union(set(self.adjacent8_coordinates(coord)))

        return list(node_adjacents)

    def is_part_number(self, node: NumberNode) -> bool:
        for coord in self.node_adjacents(node):
            if self.is_part_digit(coord):
                return True

        return False

    def sum_part_numbers(self) -> int:
        return sum([node.number for node in self.nodes if self.is_part_number(node)])

    def compute_gear_adjacents(self) -> None:
        for gear in self.gears:
            gear.adjacent_numbers = []

        for node in self.nodes:
            for coord in self.node_adjacents(node):
                if self.is_adjacent_to_gear(coord):
                    gear = self.gear_by_coord(coord)
                    if gear:
                        gear.adjacent_numbers.append(node)
        return

    def sum_of_gear_ratios(self) -> int:
        self.compute_gear_adjacents()
        return sum([gear.gear_ratio() for gear in self.gears])


def create_node(line_text: str, line_number: int, col_start: int, col_end: int) -> NumberNode:
    return NumberNode(
        id=f"{line_number},{col_start}",
        number=int(line_text[col_start:col_end]),
        line_number=line_number,
        col_start=col_start,
        col_end=col_end,
        line_text=line_text,
    )


def gear_id(line, column):
    return f"{line},{column}"


def parse_line(matrix: List[str], line_number: int, gear_character="*") -> List[NumberNode]:
    if line_number < 0 or line_number >= len(matrix):
        raise Exception(f"Invalid line number: {line_number}")
    col_start, col_end = None, None
    text = matrix[line_number]
    number_nodes = []
    gear_nodes = []
    for column, char in enumerate(text):
        if char == gear_character:
            gear_nodes.append(
                GearNode(id=gear_id(line_number, column), line=line_number, column=column, adjacent_numbers=[])
            )
        if col_start is None and char.isdigit():
            col_start = column
        if col_start is not None and not char.isdigit():
            col_end = column
            number_nodes.append(create_node(text, line_number, col_start, col_end))
            col_start, col_end = None, None
    # Number finishes in the last position of the line
    if col_start is not None and col_end is None:
        col_end = len(text)
        number_nodes.append(create_node(text, line_number, col_start, col_end))
    return number_nodes, gear_nodes


def gear_ratios(filename):
    matrix = utils.read_input(filename).split("\n")
    nodes = []
    gears = []
    for line_number, _ in enumerate(matrix):
        number_nodes, gear_nodes = parse_line(matrix, line_number)
        nodes.extend(number_nodes)
        gears.extend(gear_nodes)

    matrix = Matrix(matrix, nodes, gears)
    print(matrix.sum_part_numbers())
    print(matrix.sum_of_gear_ratios())


def test_samples():
    matrix = utils.read_input("src/2023_3_gear_ratios_sample.txt").split("\n")
    # 467..114..
    assert parse_line(matrix, 0)[0] == [
        NumberNode(
            id="0,0",
            number=467,
            line_number=0,
            col_start=0,
            col_end=3,
            line_text="467..114..",
        ),
        NumberNode(
            id="0,5",
            number=114,
            line_number=0,
            col_start=5,
            col_end=8,
            line_text="467..114..",
        ),
    ]

    # 617*......
    assert parse_line(matrix, 4)[0] == [
        NumberNode(
            id="4,0",
            number=617,
            line_number=4,
            col_start=0,
            col_end=3,
            line_text="617*......",
        )
    ]

    assert parse_line(["...*...617"], 0)[0] == [
        NumberNode(
            id="0,7",
            number=617,
            line_number=0,
            col_start=7,
            col_end=10,
            line_text="...*...617",
        )
    ]


if __name__ == "__main__":
    test_samples()
    gear_ratios("src/2023_3_gear_ratios.txt")
