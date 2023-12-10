from dataclasses import dataclass
from typing import List, Tuple

import utils


@dataclass
class Card:
    number: int
    winning: List[int]
    scratch: List[int]


def parse_card_number(line: str) -> int:
    return int(line.split(":")[0].replace("Card ", ""))


def parse_numbers(numbers: str) -> List[int]:
    result = []
    for number in numbers.strip().split(" "):
        number = number.strip()
        if len(number) > 0:
            result.append(int(number.strip()))
    return result


def parse_card_winning_and_scratch(line: str) -> Tuple[List[int], List[int]]:
    numbers = line.split(":")[1]
    raw_winning, raw_scratch = numbers.split("|")
    winning = parse_numbers(raw_winning)
    scratch = parse_numbers(raw_scratch)
    return winning, scratch


def parse_card(line: str) -> Card:
    winning, scratch = parse_card_winning_and_scratch(line)
    return Card(parse_card_number(line), winning=winning, scratch=scratch)


def card_score(card: Card) -> int:
    scores = set(card.winning).intersection(set(card.scratch))
    if len(scores) == 0:
        score = 0
    else:
        score = 2 ** (len(scores) - 1)
    return score


def number_of_winning_numbers(card: Card) -> int:
    return len(set(card.winning).intersection(set(card.scratch)))


def sum_winning_scores(cards: List[Card]) -> int:
    return sum(card_score(card) for card in cards)


def sum_part_2(cards: List[Card]) -> int:
    total_scratch_cards = {}
    for card in cards:
        total_scratch_cards[card.number] = 1

    for card in cards:
        winning_numbers = number_of_winning_numbers(card)
        for i in range(card.number + 1, card.number + winning_numbers + 1):
            total_scratch_cards[i] += total_scratch_cards[card.number]

    return sum(total_scratch_cards.values())


def scratchcards(filename):
    cards = []
    for _, line in enumerate(utils.read_by_line(filename)):
        cards.append(parse_card(line))
    print(sum_winning_scores(cards))
    print(sum_part_2(cards))


def test_samples():
    assert parse_card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53") == Card(
        1, winning=[41, 48, 83, 86, 17], scratch=[83, 86, 6, 31, 17, 9, 48, 53]
    )


if __name__ == "__main__":
    test_samples()
    scratchcards("src/2023_4_scratchcards.txt")
