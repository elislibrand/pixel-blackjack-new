import pygame as pg
from src.enums import GameState
from src.enums import Suit
from src.enums import Rank
from src.engine import Screen
from src.objects import Card
from src.objects import PlacedCard
from src.engine import Game
from src.data.constants import *

class GameManager:
    def __init__(self):
        self.game = Game()
    
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.game.state == GameState.SELECT_BET:
                        self.game.state = GameState.IDLING

                        self.game.deal_cards()
                        self.game.place_bet()
                    elif self.game.state == GameState.CHOOSE_ACTION:
                        self.game.state = GameState.IDLING

                        self.game.hit()

                if event.key == pg.K_d:
                    if self.game.state == GameState.CHOOSE_ACTION:
                        self.game.state = GameState.IDLING
                        
                        self.game.double_down()

                if event.key == pg.K_s:
                    if self.game.state == GameState.CHOOSE_ACTION:
                        self.game.state = GameState.IDLING
                        
                        self.game.split()

                if event.key == pg.K_SPACE:
                    if self.game.state == GameState.CHOOSE_ACTION:
                        self.game.state = GameState.IDLING

                        self.game.stand()

                if event.key == pg.K_ESCAPE:
                    print('PAUSE')

                if event.key == pg.K_UP:
                    if self.game.state == GameState.SELECT_BET:
                        self.game.change_bet(1)
                if event.key == pg.K_DOWN:
                    if self.game.state == GameState.SELECT_BET:
                        self.game.change_bet(-1)

    def update(self):
        if self.game.state == GameState.SELECT_BET:
            pass
        elif self.game.state == GameState.CHOOSE_ACTION:
            pass

    def draw(self, screen):
        screen.fill(C_BACKGROUND)

        print('State Here: {}'.format(self.game.state.name))
        
        self.game.draw(screen)