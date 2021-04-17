from enum import Enum, auto

class GameState(Enum):
    SELECT_BET = auto()
    CHOOSE_ACTION = auto()
    IDLING = auto()