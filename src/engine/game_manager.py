from src.engine import Game
from src.enums import GameState

class GameManager:
    def __init__(self):
        self.state = GameState.SELECT_BET

    def update(self, key):
        if self.state == GameState.SELECT_BET:
            pass
        elif self.state == GameState.CHOOSE_ACTION:
            pass