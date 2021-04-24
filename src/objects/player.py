from src.objects import Hand
from src.data.constants import *

class Player:
    def __init__(self):
        self.chips = P_STARTING_CHIPS
        self.last_bet = BET_STEP

    def build(self):
        self.hands = [Hand()]

        if self.last_bet > self.chips:
            self.bet = self.chips
        else:
            self.bet = self.last_bet
            
    def get_next_card_pos(self):
        n_cards = self.hands[0].n_cards
        
        return (
            P_CARD_STARTING_POS[0] + (n_cards * P_CARD_STACK_OFFSET[0]), 
            P_CARD_STARTING_POS[1] - (n_cards * P_CARD_STACK_OFFSET[1])
        )
        
    def has_blackjack(self):
        return self.hands[0].value == 21 and len(self.hands[0].cards) == 2

    def draw_hands(self, screen):
        for card in self.hands[0].cards:
            card.draw(screen)

    def reset(self):
        self.build()