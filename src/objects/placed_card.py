from src.engine import assets
from src.engine import Screen
from src.objects import Card
from src.enums import Rank
from src.enums import Suit

class PlacedCard(Card):
    def __init__(self, card: Card, pos, is_rotated: bool = False, is_visible: bool = True):
        super().__init__(card.suit, card.rank)

        self.pos = pos
        self.image = assets.cards['{}{}'.format(card.rank.name, card.suit.name).lower()] if is_visible else assets.cards['facedown']

    def set_visible(self):
        self.image = assets.cards['{}{}'.format(self.rank.name, self.suit.name).lower()]

    def draw(self, screen: Screen):
        screen.blit(self.image, (self.pos[0], self.pos[1]))