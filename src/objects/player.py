from src.objects import Hand
from src.data.constants import *

class Player:
    def __init__(self):
        self.chips = P_STARTING_CHIPS
        self.last_bet = BET_STEP

    def build(self):
        self.hands = [Hand(is_active = True) if i == 0 else Hand() for i in range(len(P_HANDS_POS))]

        self.active_hand = self.hands[0]
        self.active_hand_index = 0

        if self.last_bet > self.chips:
            self.bet = self.chips
        else:
            self.bet = self.last_bet
            
    def get_next_card_pos(self, hand: Hand, offset = (0, 0)):
        index = self.hands.index(hand)
        
        n_cards = len(self.hands[index].cards)

        pos = P_HANDS_POS[self.get_n_active_hands() - 1][index]
        
        return (
            int(pos[0] + (n_cards * P_CARD_STACK_OFFSET[0]) + offset[0]), 
            int(pos[1] - (n_cards * P_CARD_STACK_OFFSET[1]) + offset[1])
        )

    def get_n_active_hands(self):
        return len([hand for hand in self.hands if hand.is_active])

    def activate_hand_with_index(self, index: int):
        self.active_hand_index = index
        self.active_hand = self.hands[index]
        
        self.hands[index].activate()

    def is_on_last_hand(self):
        return self.active_hand == self.hands[0]

    def go_to_next_hand(self):
        self.active_hand_index -= 1        
        self.active_hand = self.hands[self.active_hand_index]

    def is_next_hand_active(self):
        next_hand_index = self.active_hand_index + 1

        return self.hands[next_hand_index].is_active

    def move_hands(self, hand: Hand):
        src_index = self.hands.index(hand)
        
        if(self.hands[src_index + 1].is_active):
            self.move_hands(self.hands[src_index + 1])
        
        self.hands[src_index] = self.hands[src_index + 1] # Move unused hand forwards

        self.hands[src_index + 1] = hand        

    def has_blackjack(self):
        return self.hands[0].value == 21 and len(self.hands[0].cards) == 2

    def draw_hands(self, screen):
        max_n_cards = max([len(hand.cards) for hand in self.hands])

        for i in range(max_n_cards):
            for hand in self.hands:
                if i < len(hand.cards):
                    hand.cards[i].draw(screen)

    def reset(self):
        self.build()