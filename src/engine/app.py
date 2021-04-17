import pygame as pg
import sys
from os import path, environ
from src.engine import Screen
from src.engine import assets
from src.data.constants import *

# TESTING
from src.objects import Card, PlacedCard
from src.enums import Suit, Rank

class App:
    def __init__(self):
        pg.init()

        environ['SDL_VIDEO_CENTERED'] = '1'

        self.clock = pg.time.Clock()

        self.build()

    def build(self):
        assets.load()

        pg.display.set_caption('{} (v{})'.format(G_TITLE, G_VERSION))
        pg.mouse.set_visible(False)

        self.fps = assets.settings['fps']
        self.screen = Screen((assets.settings['window']['width'], assets.settings['window']['height']), assets.settings['window']['mode'])

    def run(self):
        self.is_playing = True

        while self.is_playing:
            self.clock.tick(self.fps)
            
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
        pg.display.set_caption('{} (v{}) [FPS: {}]'.format(G_TITLE, G_VERSION, int(self.clock.get_fps())))
        
        self.screen.window.fill(C_BACKGROUND)
        #self.screen.window.blit(assets.cards['acespades'], assets.cards['acespades'].get_size())

        card = Card(Suit.HEARTS, Rank.ACE)
        placed_card = PlacedCard(card)

        placed_card.draw_to(self.screen)

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()