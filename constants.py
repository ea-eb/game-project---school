"""
This file contains all the variables that DO NOT CHANGE ANYWHERE in the code
Variables that do not change anywhere are called Constants
Constants usually have an uppercase notation (common programming practice)
"""

import os

__path = r"C:\Users\eb174\Desktop\main computer science programming project"

PATHS = {
    "menu": {
        "high_score": os.path.join(__path, "high_score.bin"),
        "background": os.path.join(__path, "sprites", "menu", "background.PNG"),
        "controls_button": os.path.join(__path, "sprites", "menu", "controls_button.PNG"),
        "high_score_button": os.path.join(__path, "sprites", "menu", "high_score_button.PNG"),
        "play_game_button": os.path.join(__path, "sprites", "menu", "play_game_button.PNG"),
        "quit_game_button": os.path.join(__path, "sprites", "menu", "quit_game_button.PNG"),
    },
    "player": {
        "left": [
            os.path.join(__path, "sprites", "player", "left_still.png"),
            os.path.join(__path, "sprites", "player", "left_1.png"),
            os.path.join(__path, "sprites", "player", "left_2.png"),
            os.path.join(__path, "sprites", "player", "left_3.png"),
        ],
        "right": [
            os.path.join(__path, "sprites", "player", "right_still.png"),
            os.path.join(__path, "sprites", "player", "right_1.png"),
            os.path.join(__path, "sprites", "player", "right_2.png"),
            os.path.join(__path, "sprites", "player", "right_3.png"),
        ],
    },
    "enemy_1": {
        "left": [
            os.path.join(__path, "sprites", "enemy_1", "left_still.png"),
            os.path.join(__path, "sprites", "enemy_1", "left_1.png"),
            os.path.join(__path, "sprites", "enemy_1", "left_2.png"),
            os.path.join(__path, "sprites", "enemy_1", "left_3.png"),
        ],
        "right": [
            os.path.join(__path, "sprites", "enemy_1", "right_still.png"),
            os.path.join(__path, "sprites", "enemy_1", "right_1.png"),
            os.path.join(__path, "sprites", "enemy_1", "right_2.png"),
            os.path.join(__path, "sprites", "enemy_1", "right_3.png"),
        ],
    },
    "map": {
        "bush": os.path.join(__path, "sprites", "bush.png"),
        "coin": os.path.join(__path, "sprites", "beer.png"),
        "health": os.path.join(__path, "sprites", "pizza.png"),
        "powerup": os.path.join(__path, "sprites", "hat.png")
    }
}

COLORS = {
    "text": (255, 255, 255),
    "back_button": (100, 100, 100),
    "background": (46, 139, 87)
}

SCREEN_HEIGHT = 729
SCREEN_WIDTH = 728

# Frames per second
FPS = 60

GAME_TIME = 5 * 60

MAP_1 = [
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, "bush", None, "bush", None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, "bush", None, None, None, None, None, None, "health", None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, "coin", None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
]


MAP_2 = [
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, "bush", None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, "coin", None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
]

GAME_WORLDS = [MAP_1, MAP_2]