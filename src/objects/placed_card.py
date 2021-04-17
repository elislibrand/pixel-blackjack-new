from src.engine import assets
from src.engine import Screen
from src.objects import Card
from src.enums import Rank
from src.enums import Suit

class PlacedCard(Card):
    def __init__(self, card: Card):
        super().__init__(card.suit, card.rank)
        
        self.x = 0
        self.y = 0
        self.image = assets.cards['{}{}'.format(card.rank.name, card.suit.name).lower()]

    def draw_to(self, screen: Screen):
        screen.window.blit(self.image, (self.x, self.y))