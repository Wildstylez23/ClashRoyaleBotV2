"""
Defines the possible states for the bot's main loop (state machine).
"""
from enum import Enum, auto


class GameState(Enum):
    """Enumeration for the bot's current state."""
    INITIALIZING = auto()
    ON_MENU = auto()
    IN_BATTLE = auto()
    POST_GAME = auto()
    STOPPED = auto()
