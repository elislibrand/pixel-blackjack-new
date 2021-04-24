import pygame as pg
from src.engine import assets
from src.engine import Screen
from src.objects import Card
from src.enums import Rank
from src.enums import Suit
from src.data.constants import *
from math import cos, radians

class PlacedCard(Card):
    def __init__(self, card: Card, pos, rotation = (0, 0, 0), is_visible: bool = True):
        super().__init__(card.suit, card.rank)

        self.pos = pos
        self.rotation = rotation

        if card.rank is None:
            self.image = assets.cards['cut']
        elif is_visible:
            self.image = assets.cards['{}{}'.format(card.rank.name, card.suit.name).lower()]
        else:
            self.image = assets.cards['facedown']

        self.update_rotation()
    
    def set_visible(self):
        self.image = assets.cards['cut'] if self.rank is None else assets.cards['{}{}'.format(self.rank.name, self.suit.name).lower()]

    def update_rotation(self):
        width_x = int(CARD_SIZE[0] * abs(cos(radians(self.rotation[1]))))
        width_y = int(CARD_SIZE[1] * abs(cos(radians(self.rotation[0]))))
        
        image = pg.transform.scale(self.image, (width_x if width_x > 0 else 1, width_y if width_y > 0 else 1))

        self.transformed_image = pg.transform.rotate(image, self.rotation[2])

    def draw(self, screen: Screen):
        screen.blit(self.transformed_image, (self.pos[0], self.pos[1]))