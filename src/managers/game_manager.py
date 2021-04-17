import pygame as pg
from src.enums import GameState
from src.enums import Suit
from src.enums import Rank
from src.data.constants import *
from src.engine import Screen
from src.objects import Card
from src.objects import PlacedCard

from src.engine import Game

class GameManager:
    def __init__(self):
        self.state = GameState.SELECT_BET

        self.game = Game(self.state)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.state == GameState.SELECT_BET:
                        self.game.deal_cards()
                        self.game.place_bet()

                        self.state = GameState.IDLING
                    if self.state == GameState.CHOOSE_ACTION:
                        self.game.hit()

                        self.state = GameState.IDLING
                if event.key == pg.K_d:
                    if self.state == GameState.CHOOSE_ACTION:
                        self.game.double_down()

                        self.state = GameState.IDLING
                if event.key == pg.K_s:
                    if self.state == GameState.CHOOSE_ACTION:
                        self.game.split()

                        self.state = GameState.IDLING
                if event.key == pg.K_SPACE:
                    if self.state == GameState.CHOOSE_ACTION:
                        self.game.stand()

                        self.state = GameState.IDLING
                if event.key == pg.K_ESCAPE:
                    print('PAUSE')
                if event.key == pg.K_UP:
                    if self.state == GameState.SELECT_BET:
                        self.game.change_bet(1)
                if event.key == pg.K_DOWN:
                    if self.state == GameState.SELECT_BET:
                        self.game.change_bet(-1)

    def update(self):
        if self.state == GameState.SELECT_BET:
            pass
        elif self.state == GameState.CHOOSE_ACTION:
            pass

    def draw(self, screen):
        screen.window.fill(C_BACKGROUND)
        
        self.game.draw(screen)