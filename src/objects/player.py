from src.objects import Hand

class Player:
    def __init__(self):
        self.chips = 50
        
    def build(self):
        self.hands = [Hand()]

        self.bet = 0

        self.is_blackjack = False
    
    def reset(self):
        self.build()