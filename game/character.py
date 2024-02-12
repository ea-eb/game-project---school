import pygame
import constants
import math

class Character:

    def __init__(self, path: dict, screen: pygame.Surface, speed: float = 1.4, x_pos: int = 100, y_pos: int = 100):
        """
        This class is used to create a character

        Parameters:
            - paths - all of the paths for the menu (reference - constants.PATHS["player"])
            - screen - the pygame screen that will visualize the menu
            - speed - how fast the character should move on the screen
            - x_pos - the X position to spawn the character
            - y_pos - the Y postiion to spawn the character
        """
        self.screen = screen

        # How fast the character will move on the screen
        self.speed = speed

        # Get only the still image
        self.left_still = pygame.image.load(path["left"][0]).convert_alpha()

        # Get the walking animation only
        self.left_walk = [pygame.image.load(file_path).convert_alpha() for file_path in path["left"][1:]]

        # Get only the still image
        self.right_still = pygame.image.load(path["right"][0]).convert_alpha()

        # Get the walking animation only
        self.right_walk = [pygame.image.load(file_path).convert_alpha() for file_path in path["right"][1:]]
        
        # Store the current frame
        self.frame = self.left_still

        # Create a rectangle from A SINGLE image
        # We will move the rectangle with the image
        self.rect = self.frame.get_rect(center=(x_pos, y_pos))

        # Store the current frame that will be shown
        self.__index = 0



    def __update_frame(self, postion: str):
        """
        Change the character's animation

        Parameters:
            - postion - either left or right to execute the right animation
        """
        if postion not in ["left", "right"]:
            return
                
        if len(self.left_walk) - 1 <= self.__index:
            self.__index = 0
        else:
            self.__index += 0.1

        if postion == "left":
            self.frame = self.left_walk[int(self.__index)]
        
        if postion == "right":
            self.frame = self.right_walk[int(self.__index)]        


    def move_left(self):
        self.rect.x -= self.speed
        self.__update_frame("left")

    def move_right(self):
        self.rect.x += self.speed
        self.__update_frame("right")

    def move(self):
        pass


class Player(Character):

    def __init__(self, path: dict, screen: pygame.Surface, speed: float = 1.4, x_pos: int = 100, y_pos: int = 100):
        # Run the __init__ in Character with the given parameters
        super().__init__(path, screen, speed, x_pos, y_pos)


    def move(self):
        """
        Move the character in X and Y coordinates.
        The character does not run outside of the screen
        """     
        keys = pygame.key.get_pressed()

        character_width = self.frame.get_width()
        character_height = self.frame.get_height()

        # Check if character has bumped into the left side of the window
        left_side = -(character_width // 3) <= self.rect.x
        # Check if character has bumped into the right side of the window
        right_side = (constants.SCREEN_WIDTH - character_width) >= self.rect.x
        # Check if character has bumped into the up side of the window
        up_side = 0 <= self.rect.y
        # Check if character has bumped into the down side of the window
        down_side = (constants.SCREEN_HEIGHT - character_height) >= self.rect.y

        # Move left
        if keys[pygame.K_a] and left_side:
            self.move_left()
        
        # Move right
        elif keys[pygame.K_d] and right_side:
            self.move_right()

        # Move up
        elif keys[pygame.K_w] and up_side:
            self.rect.y -= self.speed

        # Move down
        elif keys[pygame.K_s] and down_side:
            self.rect.y += self.speed

        # Move the position so there is no lag
        self.screen.blit(self.frame, self.rect)
        

class Enemy(Character):

    def __init__(self, path: dict, screen: pygame.Surface, speed: float = 1.4, x_pos: int = 100, y_pos: int = 100, follow_threshold: int = 200, follow_speed: float = 0.5):
        super().__init__(path, screen, speed, x_pos, y_pos)

        self.follow_threshold = follow_threshold
        self.follow_speed = follow_speed


    def __get_distance(self, player: Player) -> float:
        return math.sqrt((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2)


    def move(self, player: Player):
        

        distance = self.__get_distance(player)

        in_distance = distance <= self.follow_threshold

        left_difference = player.rect.right - self.rect.left
        if (left_difference >= -10 and left_difference <= 50) and in_distance:
            self.move_left()
        
        right_difference = player.rect.left - self.rect.right
        if (right_difference <= 10 and right_difference >= -50) and in_distance:
            self.move_right()

        
        up_difference = player.rect.bottom - self.rect.top
        if (up_difference <= 30 and up_difference >= -30) and in_distance:
            self.rect.y -= self.speed
            
        
        down_difference = player.rect.top - self.rect.bottom
        if (down_difference <= 30 and down_difference >= -30) and in_distance:
            self.rect.y += self.speed

        # Move the position so there is no lag
        self.screen.blit(self.frame, self.rect)