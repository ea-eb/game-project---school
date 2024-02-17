"""
Hold custom data types that are used within the game
"""
from enum import Enum

class State(Enum):

    GAME: str = "game"
    HIGH_SCORE: str = "high score"
    QUIT: str = "quit"
    CONTROLS: str = "controls"
    NOTHING: str = "none" # For consistency, otherwise None works as well


class CollisionDirection(Enum):

    LEFT: str = "left"
    RIGHT: str = "right"
    UP: str = "up"
    DOWN: str = "down"
    NONE: str = "none"