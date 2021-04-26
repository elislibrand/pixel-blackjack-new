import random
from src.objects import Card
from src.enums import Rank
from src.enums import Suit

class Deck:
    def __init__(self):
        self.cards = []

    def create(self, n_decks: int = 1):
        self.cards = [Card(suit, rank.TWO) for suit in Suit for rank in Rank for i in range(n_decks)]

    def shuffle(self):
        random.shuffle(self.cards)

    def add_cut_card(self):
        self.cards.insert(random.randint(int((len(self.cards) * 0.15) - 1), int((len(self.cards) * 0.3)) - 1), Card(None, None))

    def take_card(self):
        return self.cards.pop()