from src.enums import Rank
from src.enums import Suit

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def get_value(self):
        if self.rank is None:
            return 0

        if self.rank == Rank.ACE:
            return 1
        
        if self.rank == Rank.JACK or self.rank == Rank.QUEEN or self.rank == Rank.KING:
            return 10
        
        return int(self.rank.value)

    def is_cut_card(self):
        return self.rank is None