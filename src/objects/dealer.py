from src.objects import Deck
from src.objects import Hand

class Dealer:
    def __init__(self):
        self.playing_deck = Deck()

        self.should_shuffle = True
        
    def build(self):
        self.hand = Hand()

        if self.should_shuffle:
            self.shuffle_playing_deck()

            self.should_shuffle = False
    
    def shuffle_playing_deck(self):
        print('Shuffling...')
        
        self.playing_deck.create(n_decks = 6)
        self.playing_deck.shuffle()
        self.playing_deck.add_cut_card()

    def draw_card(self):
        card = self.playing_deck.draw_card()
        
        if card.get_value() == 0:
            self.should_shuffle = True

            card = self.playing_deck.draw_card()

        return card

    def has_blackjack(self):
        return self.hand.value == 21 and len(self.hand.cards) == 2

    def reset(self):
        self.build()