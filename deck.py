import random
from card import Card
from suit import Suit
from rank import Rank

class Deck:
    def __init__(self):
        self.cards = []

    def create(self):
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def print(self):
        for card in self.cards:
            print('{}{}'.format(card.suit.value, card.rank.value))