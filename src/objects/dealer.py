from src.objects import Deck
from src.objects import Hand

class Dealer:
    def __init__(self):
        self.playing_deck = Deck()

        self.should_shuffle = True
        self.cut_card = None
        
    def build(self):
        self.hand = Hand()

        if self.should_shuffle:
            self.shuffle_playing_deck()

            self.should_shuffle = False
    
    def shuffle_playing_deck(self):        
        self.playing_deck.create(n_decks = 6)
        self.playing_deck.shuffle()
        self.playing_deck.add_cut_card()

        self.cut_card = None

    def draw_card(self):
        return self.playing_deck.draw_card()

    def has_blackjack(self):
        return self.hand.value == 21 and len(self.hand.cards) == 2

    def reset(self):
        self.build()