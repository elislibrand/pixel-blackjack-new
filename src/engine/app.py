import pygame as pg
import sys
from os import path, environ
from src.engine import Screen
from src.engine import assets
from src.managers import GameManager
from src.data.constants import *

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

        self.game_manager = GameManager() # Initializing of managers need work

        while self.is_playing:
            self.clock.tick(self.fps)
            
            self.handle_events()
            self.update()
            self.draw()

        self.quit()

    def handle_events(self):
        events = pg.event.get()
        
        for event in events:
            if event.type == pg.QUIT:
                self.is_playing = False

        self.game_manager.handle_events(events)

    def update(self):
        self.game_manager.update()

    def draw(self):
        pg.display.set_caption('{} (v{}) [FPS: {}]'.format(G_TITLE, G_VERSION, int(self.clock.get_fps())))
        
        self.game_manager.draw(self.screen)

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()