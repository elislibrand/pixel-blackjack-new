import pygame as pg
from src.engine import assets
from src.data.constants import *

class Screen:
    def __init__(self):
        # This function needs to be changed to add windowed borderless and windowed mode
        #size = (G_SIZE[0] * assets.settings['window']['scale'], G_SIZE[1] * assets.settings['window']['scale'])
        mode = ''#assets.settings['window']['mode']
        
        if mode == 'fullscreen':
            flag = pg.FULLSCREEN
        elif mode == 'windowed_borderless':
            flag = pg.NOFRAME
        else:
            flag = 0

        self.window = pg.display.set_mode((640, 360), flags = flag)

        if assets.settings['window']['auto_scale']:
            width, height = pg.display.get_window_size()

            scale = min(int(width / G_SIZE[0]), int(height / G_SIZE[1]))

            assets.settings['window']['scale'] = scale