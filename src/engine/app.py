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

        self.refresh_rate = assets.settings['refresh_rate']
        self.screen = Screen()

    def run(self):
        self.is_playing = True

        self.game_manager = GameManager() # Initializing of managers need work

        while self.is_playing:
            self.clock.tick(self.refresh_rate)
            
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

        draw_area = pg.Surface(G_SIZE)
        
        self.game_manager.draw(draw_area)
        
        draw_area = pg.transform.scale(draw_area, (G_SIZE[0] * assets.settings['window']['scale'], G_SIZE[1] * assets.settings['window']['scale']))
        
        #self.screen.window.blit(draw_area, draw_area.get_rect())
        self.screen.window.blit(draw_area, pg.Rect(
            int((self.screen.window.get_width() - draw_area.get_width()) / 2), 
            int((self.screen.window.get_height() - draw_area.get_height()) / 2), 
            draw_area.get_width(),
            draw_area.get_height()
        ))

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()