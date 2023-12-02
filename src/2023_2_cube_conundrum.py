from dataclasses import dataclass
from typing import List

import utils


@dataclass
class GameSet:
    red: int = 0
    blue: int = 0
    green: int = 0

    def is_valid(self, max_red, max_green, max_blue) -> bool:
        # A set is valid if all colors are below or equal their max
        return self.red <= max_red and self.blue <= max_blue and self.green <= max_green


@dataclass
class Game:
    number: int
    sets: List[GameSet]

    def is_valid(self, max_red, max_green, max_blue) -> bool:
        # A game is valid if all sets are valid
        return all([set.is_valid(max_red, max_green, max_blue) for set in self.sets])

    def max_per_color(self) -> GameSet:
        return GameSet(
            red=max([set.red for set in self.sets]),
            blue=max([set.blue for set in self.sets]),
            green=max([set.green for set in self.sets]),
        )

    def power_set(self) -> int:
        maximums = self.max_per_color()
        return maximums.red * maximums.blue * maximums.green


def parse_set(game_set: str) -> GameSet:
    # 3 blue, 4 red
    samples = game_set.split(",")
    result = GameSet()
    for sample in samples:
        count, color = sample.strip().split(" ")
        if color == "red":
            result.red = int(count)
        elif color == "blue":
            result.blue = int(count)
        elif color == "green":
            result.green = int(count)
    return result


def parse_sets(line: str) -> List[GameSet]:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    parts = line.split(":")
    sets = []
    for game_set in parts[1].split(";"):
        sets.append(parse_set(game_set))
    return sets


def parse_game_number(line: str) -> int:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    parts = line.split(":")
    return int(parts[0].split(" ")[1])


def parse_game(line: str) -> Game:
    game_number = parse_game_number(line)
    game_sets = parse_sets(line)
    return Game(number=game_number, sets=game_sets)


def sum_valid_game_numbers(
    games: List[Game], max_red: int, max_green: int, max_blue: int
) -> int:
    return sum(
        [game.number for game in games if game.is_valid(max_red, max_green, max_blue)]
    )


def sum_game_power_set(games: List[Game]) -> int:
    return sum([game.power_set() for game in games])


def cube_conundrum(filename):
    MAX_RED = 12
    MAX_GREEN = 13
    MAX_BLUE = 14
    games = []
    for line in utils.read_by_line(filename):
        games.append(parse_game(line))

    print(sum_valid_game_numbers(games, MAX_RED, MAX_GREEN, MAX_BLUE))
    print(sum_game_power_set(games))


def test_samples():
    assert parse_set("3 blue, 4 red") == GameSet(red=4, blue=3, green=0)
    assert parse_set("1 red, 2 green, 6 blue") == GameSet(red=1, blue=6, green=2)
    assert (
        parse_game_number("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == 1
    )
    assert parse_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == Game(
        number=1,
        sets=[
            GameSet(red=4, blue=3, green=0),
            GameSet(red=1, blue=6, green=2),
            GameSet(red=0, blue=0, green=2),
        ],
    )


if __name__ == "__main__":
    test_samples()
    cube_conundrum("src/2023_2_cube_conundrum.txt")
