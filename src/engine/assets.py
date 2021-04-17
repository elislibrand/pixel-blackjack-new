import pygame as pg
import json
from os import path, listdir

cards = {}
fonts = {}
audio = {}
settings = {}

source_folder = path.dirname(path.join(path.dirname(__file__), '../../'))

def load():
    load_cards()
    load_fonts()
    #load_audio()
    load_settings()

def load_cards():
    global cards, source_folder

    cards_folder = path.join(source_folder, 'assets/images/cards')
    
    file_names = [f for f in listdir(cards_folder) if path.isfile(path.join(cards_folder, f))]
    
    for file_name in file_names:
        cards[path.splitext(file_name)[0]] = to_image(path.join(cards_folder, file_name))

def load_fonts():
    global fonts, source_folder

    fonts_folder = path.join(source_folder, 'assets/fonts')

    file_names = [f for f in listdir(fonts_folder) if path.isfile(path.join(fonts_folder, f))]
    
    for file_name in file_names:
        fonts[path.splitext(file_name)[0]] = to_font(path.join(fonts_folder, file_name))

def load_audio():
    global audio, source_folder

    audio_folder = path.join(source_folder, 'assets/audio')

def load_settings():
    global settings, source_folder

    settings_folder = path.join(source_folder, 'assets/data')

    with open(path.join(settings_folder, 'settings.json'), 'r') as f:
        settings = json.load(f)
        
def to_image(file_path: str):
    return pg.image.load(file_path)

def to_font(file_path: str, size: int = 6):
    return pg.font.Font(file_path, size)

def to_audio(file_path: str):
    pass