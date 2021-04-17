import pygame as pg
import sys
from os import path
from src.engine import Screen
from src.engine import assets

# TESTING
from src.objects import Card, PlacedCard
from src.enums import Suit, Rank

class App:
    def __init__(self, screen: Screen):
        pg.init()

        pg.display.set_caption('Pixel Blackjack (FPS: 60)')
        pg.mouse.set_visible(False)

        self.screen = screen
        self.clock = pg.time.Clock()

        self.load_data()

    def load_data(self):
        assets.load()

    def run(self):
        self.is_playing = True

        while self.is_playing:
            self.clock.tick(60)
            
            self.handle_events()
            self.update()
            self.draw()

        self.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_playing = False

    def update(self):
        pass

    def draw(self):
        pg.display.set_caption('Pixel Blackjack (FPS: {})'.format(int(self.clock.get_fps())))
        
        self.screen.window.fill((48, 102, 60))
        #self.screen.window.blit(assets.cards['acespades'], assets.cards['acespades'].get_size())

        card = Card(Suit.HEARTS, Rank.ACE)
        placed_card = PlacedCard(card)
        
        placed_card.draw_to(self.screen)

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()