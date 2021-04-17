import pygame as pg
from screeninfo import get_monitors
from src.engine import assets
from src.data.constants import *

class Screen:
    def __init__(self):
        if assets.settings['window']['auto_scale']:
            width, height = get_monitors()[0].width, get_monitors()[0].height

            scale = min(int(width / G_SIZE[0]), int(height / G_SIZE[1]))

            assets.settings['window']['scale'] = scale
        
        size = (G_SIZE[0] * assets.settings['window']['scale'], G_SIZE[1] * assets.settings['window']['scale'])
        mode = assets.settings['window']['mode']
        
        if mode == 'fullscreen':
            flag = pg.FULLSCREEN
        elif mode == 'windowed_borderless':
            flag = pg.NOFRAME
        else:
            flag = 0

        self.window = pg.display.set_mode(size, flag)