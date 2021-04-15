from src.engine import Card
from src.enums import Rank
from src.enums import Suit

class Hand:
    def __init__(self):
        self.build()

    def build(self):
        self.cards = []

        self.value = 0

        self.is_soft = False

    def calculate_value(self):
        value = 0
        n_aces = 0

        for card in self.cards:
            if card.rank == Rank.ACE:
                n_aces += 1
            elif card.rank == Rank.JACK or card.rank == Rank.QUEEN or card.rank == Rank.KING:
                value += 10
            else:
                value += int(card.rank.value)

        for i in range(n_aces):
            if value + (n_aces - 1) > 10:
                value += 1
            else:
                value += 11

                self.is_soft = True

        self.value = value

    def reset(self):
        self.build()