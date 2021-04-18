from src.objects import Deck
from src.objects import Hand

class Dealer:
    def __init__(self):
        self.playing_deck = Deck()
        
    def build(self):
        self.hand = Hand()
    
    def shuffle_playing_deck(self):
        self.playing_deck.create(n_decks = 6)
        self.playing_deck.shuffle()

    def has_blackjack(self):
        return self.hand.value == 21 and len(self.hand.cards) == 2

    def reset(self):
        self.build()