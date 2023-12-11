from collections import Counter
from enum import Enum

import utils


class HandLabel(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class CamelCards:
    def __init__(self, filename, with_jokers=True):
        self.hands = []
        self.with_jokers = with_jokers
        self.parse_file(filename)

    def parse_file(self, filename):
        lines = utils.read_by_line(filename)
        for line in lines:
            if self.with_jokers:
                self.hands.append(HandWithJoker(line))
            else:
                self.hands.append(Hand(line))

    def compute_total_winnings(self) -> int:
        hands = sorted(self.hands)
        winnings = 0
        for i, hand in enumerate(hands):
            rank = i + 1
            winnings += hand.bid * rank
        return winnings


class Hand:
    def __init__(self, raw_hand: str):
        cards, bid = raw_hand.split(" ")
        self.cards_rank = {
            "A": 13,
            "K": 12,
            "Q": 11,
            "J": 10,
            "T": 9,
            "9": 8,
            "8": 7,
            "7": 6,
            "6": 5,
            "5": 4,
            "4": 3,
            "3": 2,
            "2": 1,
        }
        self.raw_cards: str = cards
        self.bid: int = int(bid)
        self.cards = cards
        self.label: HandLabel = self.assign_label(cards)

    def __lt__(self, other):
        if self.label.value == other.label.value:
            for i in range(len(self.cards)):
                self_card = self.cards[i]
                other_card = other.cards[i]
                if self.cards_rank[self_card] != self.cards_rank[other_card]:
                    return self.cards_rank[self_card] < self.cards_rank[other_card]
        else:
            return self.label.value < other.label.value

    def assign_label(self, raw_hand: str) -> HandLabel:
        counts = Counter(raw_hand)
        if self.is_five_of_a_kind(counts):
            return HandLabel.FIVE_OF_A_KIND
        elif self.is_four_of_a_kind(counts):
            return HandLabel.FOUR_OF_A_KIND
        elif self.is_full_house(counts):
            return HandLabel.FULL_HOUSE
        elif self.is_three_of_a_kind(counts):
            return HandLabel.THREE_OF_A_KIND
        elif self.is_two_pair(counts):
            return HandLabel.TWO_PAIR
        elif self.is_one_pair(counts):
            return HandLabel.ONE_PAIR
        elif self.is_high_card(counts):
            return HandLabel.HIGH_CARD

    def is_five_of_a_kind(self, counts) -> bool:
        common = counts.most_common(2)
        if len(common) == 1 and common[0][1] == 5:
            return True
        return False

    def is_four_of_a_kind(self, counts) -> bool:
        common = counts.most_common(5)
        if len(common) == 2 and common[0][1] == 4:
            return True
        return False

    def is_full_house(self, counts) -> bool:
        common = counts.most_common(5)
        if len(common) == 2 and common[0][1] == 3 and common[1][1] == 2:
            return True
        return False

    def is_three_of_a_kind(self, counts) -> bool:
        common = counts.most_common(5)
        if len(common) == 3 and common[0][1] == 3:
            return True
        return False

    def is_two_pair(self, counts) -> bool:
        common = counts.most_common(5)
        if len(common) == 3 and common[0][1] == 2 and common[1][1] == 2:
            return True
        return False

    def is_one_pair(self, counts) -> bool:
        common = counts.most_common(5)
        if len(common) == 4 and common[0][1] == 2:
            return True
        return False

    def is_high_card(self, counts) -> bool:
        common = counts.most_common(5)
        if len(common) == 5:
            return True
        return False


class HandWithJoker(Hand):
    def __init__(self, raw_hand: str):
        super().__init__(raw_hand)
        self.cards_rank = {
            "A": 13,
            "K": 12,
            "Q": 11,
            "T": 10,
            "9": 9,
            "8": 8,
            "7": 7,
            "6": 6,
            "5": 5,
            "4": 4,
            "3": 3,
            "2": 2,
            "J": 1,
        }
        self.label: HandLabel = self.assign_label(self.cards)

    def assign_label(self, raw_hand: str) -> HandLabel:
        if raw_hand == "JJJJJ":
            return HandLabel.FIVE_OF_A_KIND
        counts = Counter(raw_hand.replace("J", ""))
        most_common = counts.most_common(2)
        # if the two first most commons have same count, then we replace the smallest card
        if len(most_common) >= 2 and most_common[0][1] == most_common[1][1]:
            card1 = most_common[0][0]
            card2 = most_common[1][0]
            if self.cards_rank[card1] > self.cards_rank[card2]:
                replaced_hand = raw_hand.replace("J", card1)
            else:
                replaced_hand = raw_hand.replace("J", card2)
        else:
            card, _ = most_common[0]
            replaced_hand = raw_hand.replace("J", card)
        return super().assign_label(replaced_hand)


def solution(filename):
    camel = CamelCards(filename, with_jokers=False)
    print(camel.compute_total_winnings())

    camel_jokers = CamelCards(filename, with_jokers=True)
    print(camel_jokers.compute_total_winnings())


def test_samples():
    camel = CamelCards("src/2023_07_camel_cards_sample.txt", with_jokers=False)
    assert len(camel.hands) == 5
    assert camel.hands[0].label == HandLabel.ONE_PAIR
    assert camel.hands[1].label == HandLabel.THREE_OF_A_KIND
    assert camel.hands[2].label == HandLabel.TWO_PAIR
    assert camel.hands[3].label == HandLabel.TWO_PAIR
    assert camel.hands[4].label == HandLabel.THREE_OF_A_KIND

    assert camel.compute_total_winnings() == 6440
    assert CamelCards("src/2023_07_camel_cards.txt", with_jokers=False).compute_total_winnings() == 251029473

    assert Hand("32T3K 0") < Hand("T55J5 0")


if __name__ == "__main__":
    test_samples()
    solution("src/2023_07_camel_cards_sample.txt")
    solution("src/2023_07_camel_cards.txt")
