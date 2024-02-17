from data_types import State
import pygame
import constants
import utils

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

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.__screen = screen
        
        # Fonts
        self.title_font = pygame.font.SysFont("arialblack", 58)
        
        # Load the images that we need for the menu
        self.game_font = pygame.font.SysFont("arialblack", 40)
        self.title_text = self.title_font.render("Tory Tangle",True, constants.COLORS["text"])
        self.title_text_rect = self.title_text.get_rect(center=(screen_width // 2, 50))

        # Back button
        self.back_text = self.title_font.render("Back", True, constants.COLORS["text"])
        self.back_rect = self.back_text.get_rect(center=(self.screen_width * 0.12, self.screen_height * 0.05))

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

        self.__high_score_path = paths["high_score"]

        self.state = State.NOTHING
    

    
    def interaction(self, mouse_pos: tuple[int, int]) -> State:
        """
        User can select what they want to do on the screen

        Parameters:
            - mouse_pos - the X and Y coordinates of the mouse
            
        Output:
            - state - return the game state which is needed in the main game loop
        """

        if self.play_game_button.is_clicked(mouse_pos):
            self.state = State.GAME

        elif self.high_score_button.is_clicked(mouse_pos):
            self.state = State.HIGH_SCORE

        elif self.quit_game_button.is_clicked(mouse_pos):
            self.state = State.QUIT
            
        elif self.controls_button.is_clicked(mouse_pos):
            self.state = State.CONTROLS
        
        return self.state
 

        
    def draw(self, lives: float, timer: int, coins: int, level: int):
        """
        Draw the GUI - menu, high score and controls
        """

        if self.state == State.NOTHING:
            self.__screen.blit(self.background_image, (0, 0))      
            self.__screen.blit(self.title_text, self.title_text_rect)
            
            self.controls_button.draw()
            self.high_score_button.draw()
            self.play_game_button.draw()
            self.quit_game_button.draw()

        elif self.state == State.GAME:
            lives_text = self.game_font.render(f"Lives: {lives}",True, constants.COLORS["text"])
            lives_rect = lives_text.get_rect(center=(self.screen_width * 0.15, self.screen_height * 0.95))

            minutes = timer // 60
            seconds = timer % 60
            timer_text = self.game_font.render("{:02}:{:02}".format(minutes, seconds), True, constants.COLORS["text"])
            timer_rect = timer_text.get_rect(center=(self.screen_width * 0.9, self.screen_height * 0.05))
            
            coins_text = self.game_font.render("{:02}".format(coins),True, constants.COLORS["text"])
            coins_rect = coins_text.get_rect(center=(self.screen_width * 0.07, self.screen_height * 0.05))

            level_text = self.game_font.render(f"Level {level + 1}", True, constants.COLORS["text"])
            level_rect = level_text.get_rect(center=(self.screen_width * 0.85, self.screen_height * 0.94))

            self.__screen.blit(lives_text, lives_rect)
            self.__screen.blit(timer_text, timer_rect)
            self.__screen.blit(coins_text, coins_rect)
            self.__screen.blit(level_text, level_rect)

        elif self.state == State.HIGH_SCORE:

            high_score = utils.load_high_socre(self.__high_score_path)
            text = f"Highest score: {high_score}" if high_score else "No high score found"

            high_score_text = self.title_font.render(text, True, constants.COLORS["text"])
            high_score_text_rect = high_score_text.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.5))

            self.__screen.blit(high_score_text, high_score_text_rect)
        
        elif self.state == State.CONTROLS:
            move_left_text = self.game_font.render(f"Move left: A", True, constants.COLORS["text"])
            move_left_rect = move_left_text.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.3))

            move_right_text = self.game_font.render(f"Move right: D", True, constants.COLORS["text"])
            move_right_rect = move_right_text.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.4))

            move_up_text = self.game_font.render(f"Move up: W", True, constants.COLORS["text"])
            move_up_rect = move_up_text.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.5))

            move_down_text = self.game_font.render(f"Move down: S", True, constants.COLORS["text"])
            move_down_rect = move_down_text.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.6))
            
            self.__screen.blit(move_left_text, move_left_rect)
            self.__screen.blit(move_right_text, move_right_rect)
            self.__screen.blit(move_up_text, move_up_rect)
            self.__screen.blit(move_down_text, move_down_rect)

        if self.state in [State.CONTROLS, State.HIGH_SCORE]:
            self.__screen.blit(self.back_text, self.back_rect)



    def back_button(self, mouse_pos: tuple[int, int]):
        
        if self.back_rect.collidepoint(mouse_pos):
            self.state = State.NOTHING