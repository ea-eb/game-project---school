"""
This file contains all the variables that DO NOT CHANGE ANYWHERE in the code
Variables that do not change anywhere are called Constants
Constants usually have an uppercase notation (common programming practice)
"""

import os

__sprite_path = r"C:\Users\Nikolai\Documents\GitHub\eamon\sprites"

PATHS = {
    "menu": {
        "background": os.path.join(__sprite_path, "menu", "background.PNG"),
        "controls_button": os.path.join(__sprite_path, "menu", "controls_button.PNG"),
        "high_score_button": os.path.join(__sprite_path, "menu", "high_score_button.PNG"),
        "play_game_button": os.path.join(__sprite_path, "menu", "play_game_button.PNG"),
        "quit_game_button": os.path.join(__sprite_path, "menu", "quit_game_button.PNG"),
    },
    "player": {
        "left": [
            os.path.join(__sprite_path, "player", "left_still.png"),
            os.path.join(__sprite_path, "player", "left_1.png"),
            os.path.join(__sprite_path, "player", "left_2.png"),
            os.path.join(__sprite_path, "player", "left_3.png"),
        ],
        "right": [
            os.path.join(__sprite_path, "player", "right_still.png"),
            os.path.join(__sprite_path, "player", "right_1.png"),
            os.path.join(__sprite_path, "player", "right_2.png"),
            os.path.join(__sprite_path, "player", "right_3.png"),
        ],
    },
    "enemy_1": {
        "left": [
            os.path.join(__sprite_path, "enemy_1", "left_still.png"),
            os.path.join(__sprite_path, "enemy_1", "left_1.png"),
            os.path.join(__sprite_path, "enemy_1", "left_2.png"),
            os.path.join(__sprite_path, "enemy_1", "left_3.png"),
        ],
        "right": [
            os.path.join(__sprite_path, "enemy_1", "right_still.png"),
            os.path.join(__sprite_path, "enemy_1", "right_1.png"),
            os.path.join(__sprite_path, "enemy_1", "right_2.png"),
            os.path.join(__sprite_path, "enemy_1", "right_3.png"),
        ],
    },
    "map": {
        "bush": os.path.join(__sprite_path, "bush.png")
    }
}

COLORS = {
    "text": (255, 255, 255),
    "back_button": (100, 100, 100)
}

SCREEN_HEIGHT = 729
SCREEN_WIDTH = 728

# Frames per second
FPS = 60