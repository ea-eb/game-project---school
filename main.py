"""
To do:
    - Python Typing - https://www.youtube.com/watch?v=QORvB-_mbZ0
    - How to document your code (like a chad) - https://www.youtube.com/watch?v=L7Ry-Fiij-M
    - Enums - https://www.youtube.com/watch?v=GiAHicNFvBU
    - Python 1 liners - https://www.youtube.com/watch?v=ZW-TWrEF6qc
    - Lambda functions - https://www.youtube.com/watch?v=hYzwCsKGRrg
    - @property - https://www.youtube.com/watch?v=jCzT9XFZ5bw
"""

# Import the custom written modules for the game
from menu import Menu
from game.gameplay import Gameplay
from data_types import State

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

TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)  # Fire event every second

game_menu = Menu(constants.PATHS["menu"], screen)
gameplay = Gameplay(constants.GAME_WORLDS, constants.PATHS, screen)

timer = constants.GAME_TIME

# Run the code forever
while True:

    screen.fill(constants.COLORS["background"])
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or game_menu.state == State.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == TIMER_EVENT and game_menu.state == State.GAME:
            timer -= 1 if timer > 0 else 0

        if event.type == pygame.MOUSEBUTTONDOWN and game_menu.state == State.NOTHING:
            
            game_menu.interaction(mouse_pos)
            
            if game_menu.state == State.GAME:
                timer = constants.GAME_TIME
                gameplay = Gameplay(constants.GAME_WORLDS, constants.PATHS, screen)
        
        # Check if the button left button has been pressed
        if event.type == pygame.MOUSEBUTTONDOWN and game_menu.state in [State.CONTROLS, State.HIGH_SCORE]:
            game_menu.back_button(mouse_pos)



    if game_menu.state == State.GAME:
        should_play = gameplay.play(timer)

        if not should_play:
            game_menu.state = State.NOTHING

        if timer <= 0:
            game_menu.state = State.NOTHING
    
    game_menu.draw(gameplay.player.remaining_lives, timer, gameplay.coins_collected, gameplay.next_level - 1)

    # Update the entire screen
    pygame.display.update()
    clock.tick(constants.FPS)