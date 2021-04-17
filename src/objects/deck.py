import random
from src.objects import Card
from src.enums import Rank
from src.enums import Suit

class Deck:
    def __init__(self):
        self.cards = []

    def create(self):
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)