import pygame as pg
from src.engine import assets

class Screen:
    def __init__(self, size, mode: str):
        if not isinstance(size[0], int) or not isinstance(size[1], int):
            size = (640, 360)
        
        if mode == 'fullscreen':
            flag = pg.FULLSCREEN
        elif mode == 'windowed_borderless':
            flag = pg.NOFRAME
        else:
            flag = 0

        self.window = pg.display.set_mode(size, flag)