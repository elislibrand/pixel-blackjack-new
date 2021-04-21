from src.objects import Hand
from src.data.constants import P_CARD_STARTING_POS, P_CARD_STACK_OFFSET

class Player:
    def __init__(self):
        self.chips = 50
        
    def build(self):
        self.hands = [Hand()]

        self.bet = 0

        self.is_blackjack = False
    
    def get_next_card_pos(self):
        n_cards = len(self.hands[0].cards)
        
        return (
            P_CARD_STARTING_POS[0] + (n_cards * P_CARD_STACK_OFFSET[0]), 
            P_CARD_STARTING_POS[1] + (n_cards * P_CARD_STACK_OFFSET[1])
        )
        
    def has_blackjack(self):
        if self.hands[0].value == 21 and len(self.hands[0].cards) == 2:
            self.is_blackjack = True

            return True

        return False

    def reset(self):
        self.build()