import pygame as pg

class Screen:
    def __init__(self, size = (640, 360), flag = pg.FULLSCREEN):
        self.window = pg.display.set_mode(size, flag)