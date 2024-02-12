from data_types import State
import pygame
import constants


class Button:
    
    def __init__(self, path: str, position: tuple[float, float], screen: pygame.Surface):
        """
        This class is used only in the menu screens.

        Parameters:
            - path
            - position - the X and Y coordinates of the 
            - screen - the pygame screen from pygame.display.setmode()
        """
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center = position)
        self.__screen = screen


    def draw(self):
        """
        Draw the button images on the screen
        """
        self.__screen.blit(self.image, self.rect)
    

    
    def is_clicked(self, mouse_pos: tuple[int, int]):
        """
        Check if the button has been clicked (mouse has collided with the button).

        Parameters:
            - mouse_pos - the mouse X and Y coordinates
        """
        return self.rect.collidepoint(mouse_pos)



class Menu:

    def __init__(self, paths: dict, screen: pygame.Surface, screen_width: float = constants.SCREEN_WIDTH, screen_height: float = constants.SCREEN_HEIGHT):
        """
        This class allows the player to play the game, see their high score,
        see the controls and to quit the game. 

        Parameters:
            - paths - all of the paths for the menu (reference - constants.PATHS["menu"])
            - screen - the pygame screen that will visualize the menu
            - screen_width - used for centering the text (X axis)
            - screen_height - used for centering the text (Y axis)
        """

        self.__screen = screen
        # Load the images that we need for the menu
        
        # Game text
        font = pygame.font.SysFont("arialblack", 58)
        self.text = font.render("Tory Tangle",True, constants.COLORS["text"])
        self.text_rect = self.text.get_rect(center=(screen_width // 2, 50))

        # Menu background image
        self.background_image = pygame.image.load(paths["background"]).convert_alpha()

        # Button images that the player can click on
        position = (screen_width // 2, screen_height // 2.15 + 140)
        self.controls_button = Button(paths["controls_button"], position, screen)

        position = (screen_width // 2, screen_height // 2.75 + 70)
        self.high_score_button = Button(paths["high_score_button"], position, screen)
        
        position = (screen_width // 2, screen_height // 4)
        self.play_game_button = Button(paths["play_game_button"], position, screen)
        
        position = (screen_width // 2, screen_height // 1.75 + 210)
        self.quit_game_button = Button(paths["quit_game_button"], position, screen)

    
    def interaction(self, mouse_pos: tuple[int, int]) -> State:
        """
        User can select what they want to do on the screen

        Parameters:
            - mouse_pos - the X and Y coordinates of the mouse
            
        Output:
            - state - return the game state which is needed in the main game loop
        """

        state = State.NOTHING

        if self.play_game_button.is_clicked(mouse_pos):
            state = State.GAME

        if self.high_score_button.is_clicked(mouse_pos):
            state = State.HIGH_SCORE

        if self.quit_game_button.is_clicked(mouse_pos):
            state = State.QUIT
            
        if self.controls_button.is_clicked(mouse_pos):
            state = State.CONTROLS

        return state

        
        
        
    def draw(self):
        """
        Draw the menu on the screen
        """
        self.__screen.blit(self.background_image, (0, 0))      
        self.__screen.blit(self.text, self.text_rect)
        
        self.controls_button.draw()
        self.high_score_button.draw()
        self.play_game_button.draw()
        self.quit_game_button.draw() 