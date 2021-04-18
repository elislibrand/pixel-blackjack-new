from src.objects import Hand

class Player:
    def __init__(self):
        self.chips = 50
        
    def build(self):
        self.hands = [Hand()]

        self.bet = 0

        self.is_blackjack = False
    
    def has_blackjack(self):
        if self.hands[0].value == 21 and len(self.hands[0].cards) == 2:
            self.is_blackjack = True

            return True

        return False

    def reset(self):
        self.build()