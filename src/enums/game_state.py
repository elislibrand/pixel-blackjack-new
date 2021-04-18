from enum import Enum, auto

class GameState(Enum):
    SELECT_BET = auto()
    CHOOSE_ACTION = auto()
    DEALER_SHOW = auto()
    IDLING = auto()