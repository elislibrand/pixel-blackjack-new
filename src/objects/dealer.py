from src.objects import Hand

class Dealer:
    def __init__(self):
        self.build()

    def build(self):
        self.hand = Hand()

        self.is_blackjack = False
    
    def reset(self):
        self.build()