import pygame as pg
import platform
from src.engine import assets
from src.data.constants import *

#import gi
#gi.require_version('Gdk', '3.0')
#from gi.repository import Gdk


class Screen:
    def __init__(self):
        # This function needs to be changed to add windowed borderless and windowed mode
        #size = (G_SIZE[0] * assets.settings['window']['scale'], G_SIZE[1] * assets.settings['window']['scale'])
        system = platform.system()
        
        mode = assets.settings['window']['mode']
        
        if mode == 'fullscreen':
            flag = pg.FULLSCREEN
        elif mode == 'windowed_borderless':
            flag = pg.NOFRAME
        else:
            flag = 0

        self.window = pg.display.set_mode(flags = flag, display = 0)

        if assets.settings['window']['auto_scale']:
            width, height = pg.display.get_window_size()

            scale = min(int(width / G_SIZE[0]), int(height / G_SIZE[1]))

            assets.settings['window']['scale'] = scale