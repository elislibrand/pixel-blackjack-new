import pygame as pg
import sys
from os import path

class GameEngine:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(flags = pg.FULLSCREEN)
        
        pg.display.set_caption('Pixel Blackjack (FPS: 60)')
        pg.mouse.set_visible(False)

        self.clock = pg.time.Clock()

        self.load_data()

    def load_data(self):
        game_folder = path.dirname(path.join(path.dirname(__file__), '../'))
        img_folder = path.join(game_folder, 'assets/images')

        self.test_card_img = pg.image.load(path.join(img_folder, 'cards/{}'.format('aceclubs.png')))

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
        
        self.screen.fill((48, 102, 60))
        self.screen.blit(self.test_card_img, (33, 49))

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()