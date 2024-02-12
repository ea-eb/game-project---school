"""
To do:
    - Python Typing - https://www.youtube.com/watch?v=QORvB-_mbZ0
    - How to document your code (like a chad) - https://www.youtube.com/watch?v=L7Ry-Fiij-M
    - Enums - https://www.youtube.com/watch?v=GiAHicNFvBU
    - Python 1 liners - https://www.youtube.com/watch?v=ZW-TWrEF6qc
    - Lambda functions - https://www.youtube.com/watch?v=hYzwCsKGRrg
    - @property - https://www.youtube.com/watch?v=jCzT9XFZ5bw
"""

# Import the custom written modules for the gamer
from menu import Menu
from data_types import State
from game.character import Player, Enemy
from game.map import Map

# Main file that runs the game
import constants
import pygame
import sys

# initalise pygame
pygame.init()

# set up the display for the game and the caption
screen = pygame.display.set_mode((constants.SCREEN_HEIGHT, constants.SCREEN_WIDTH))
pygame.display.set_caption("Tory Tangle") 

# define clock to set the refresh rate of the screen
clock = pygame.time.Clock()

game_menu = Menu(constants.PATHS["menu"], screen)

# Initial game state
state = State.NOTHING

bo_jo = Player(constants.PATHS["player"], screen, 3)

# wojak = Enemy(constants.PATHS["enemy_1"], screen, x_pos = 300, y_pos = 300, follow_threshold=100)


map_data = [
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, "bush", None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ]

my_map = Map(constants.PATHS["map"], map_data, screen)
my_map.create()

# Run the code forever
while True:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            state = game_menu.interaction(mouse_pos)

    
    
    # Put map here
    my_map.collide(bo_jo)
    # wojak.move(bo_jo)
    bo_jo.move()

    
    # Update the entire screen
    pygame.display.update()
    clock.tick(constants.FPS)