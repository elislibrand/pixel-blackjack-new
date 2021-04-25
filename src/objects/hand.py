from src.objects import PlacedCard
from src.enums import HandState
from src.enums import Rank
from src.enums import Suit

class Hand:
    def __init__(self, is_active: bool = False):
        self.cards = []

        self.value = 0

        self.is_active = is_active

        self.state = HandState.NO_ACE

    def add_card(self, card: PlacedCard):
        self.cards.append(card)

        self.add_value(card.get_value())

    def remove_card(self, card: PlacedCard):
        self.cards.remove(card)

        self.remove_value(card.get_value())

    def add_value(self, value: int):
        self.value += value

        if self.state == HandState.NO_ACE and value == 1:
            if self.value <= 11:
                self.value += 10
                
                self.state = HandState.SOFT
            else:
                self.state = HandState.HARD
        elif self.state == HandState.SOFT and self.value > 21:
            self.value -= 10
            
            self.state = HandState.HARD
            
    def remove_value(self, value: int):
        self.value -= value

    def activate(self):
        self.is_active = True

    '''
    def calculate_value(self):
        value = 0
        n_aces = 0
        
        for card in self.cards:
            if card.rank == Rank.ACE:
                n_aces += 1
            elif card.rank == Rank.JACK or card.rank == Rank.QUEEN or card.rank == Rank.KING:
                value += 10
            else:
                value += int(card.rank.value)

        for i in range(n_aces):
            if value + (n_aces - 1) > 10:
                value += 1
            else:
                value += 11

        self.value = value
    '''