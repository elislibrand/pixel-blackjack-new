from src.engine import GameEngine

class App:
    def __init__(self):
        self.game_engine = GameEngine()

    def run(self):
        self.game_engine.run()