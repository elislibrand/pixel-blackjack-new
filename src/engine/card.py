from src.enums import Rank
from src.enums import Suit

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank