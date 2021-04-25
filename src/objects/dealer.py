from src.engine import assets
from src.objects import Deck
from src.objects import Hand
from src.objects import Card
from src.objects import PlacedCard
from src.data.constants import *

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
        print('\nWinnings    Player    Dealer\n{}'.format('-' * 28))

        self.playing_deck.create(n_decks = 6)
        self.playing_deck.shuffle()
        self.playing_deck.add_cut_card()

        self.cut_card = None

    def take_card(self):
        return self.playing_deck.take_card()

    def get_next_card_pos(self):
        n_cards = len(self.hand.cards)

        if n_cards <= 1:
            return (
                D_CARD_STARTING_POS[0] + (n_cards * D_CARD_STACK_OFFSET[0]),
                D_CARD_STARTING_POS[1] + (n_cards * D_CARD_STACK_OFFSET[1])
            )

        return (
            D_CARD_STARTING_POS[0] - ((n_cards - 1) * D_CARD_STACK_OFFSET[0]),
            D_CARD_STARTING_POS[1] - ((n_cards - 1) * D_CARD_STACK_OFFSET[1])
        )

    def has_blackjack(self):
        return self.hand.value == 21 and len(self.hand.cards) == 2

    def should_take(self):
        return self.hand.value < 17

    def set_cut_card(self, placed_card):
        self.cut_card = placed_card

        self.should_shuffle = True

    def draw_deck(self, screen):        
        if self.playing_deck.cards[-1].rank is None:
            screen.blit(assets.cards['cut'], D_PLAYING_DECK_POS)
        else:
            screen.blit(assets.cards['facedown'], D_PLAYING_DECK_POS)

    def draw_hand(self, screen):
        for card in self.hand.cards:
            card.draw(screen)

    def reset(self):
        self.build()