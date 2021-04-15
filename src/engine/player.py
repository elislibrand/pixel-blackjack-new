from src.engine import Hand

class Player:
    def __init__(self):
        self.chips = 50
        
        self.build()

    def build(self):
        self.hands = [Hand()]

        self.is_blackjack = False
    
    def reset(self):
        self.build()