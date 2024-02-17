import pygame
import constants
import math
import random
from data_types import CollisionDirection


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


    def get_collision_direction(self, character) -> CollisionDirection:
        """
        Check if the character has collided with an object
        and if it has, get the collision direction.

        Parameters:
            - character - this class
        """
        
        left_difference = character.rect.right - self.rect.left
        if (left_difference >= -10 and left_difference <= 50):
            return CollisionDirection.LEFT

        right_difference = character.rect.left - self.rect.right
        if (right_difference <= 10 and right_difference >= -50):
            return CollisionDirection.RIGHT


        up_difference = character.rect.bottom - self.rect.top
        if (up_difference <= 30 and up_difference >= -30):
            return CollisionDirection.UP
            
        
        down_difference = character.rect.top - self.rect.bottom
        if (down_difference <= 30 and down_difference >= -30):
            return CollisionDirection.DOWN

        return CollisionDirection.NONE
    

    def collision(self, game_object):
        """
        Check if character has collided with a
        bush . Collision means you reverse
        the character's direction.

        For example - if you are going down the screen with speed 5,
        you "push" the character to go up the screen with the same speed (of 5)

        Parameters:
            - game_object - a game object from map.py
        """

        # If there is collision, then you reverse thee character's direction
        current_collision = self.get_collision_direction(game_object)
        
        if current_collision == CollisionDirection.RIGHT:
            self.rect.x -= self.speed

        if current_collision == CollisionDirection.LEFT:
            self.rect.x += self.speed

        if current_collision == CollisionDirection.UP:
            self.rect.y += self.speed

        if current_collision == CollisionDirection.DOWN:
            self.rect.y -= self.speed



class Player(Character):

    def __init__(self, 
                 path: dict, 
                 screen: pygame.Surface, 
                 speed: float = 1.4, 
                 x_pos: int = 100, 
                 y_pos: int = 100, 
                 max_lives: int = 3, 
                 damage_timeout_seconds: int = 2,
                 powerup_timeout_seconds: int = 5
                ):
        """
        This class is used to control the player

        Parameters:
            - paths - all of the paths for the menu (reference - constants.PATHS["player"])
            - screen - the pygame screen that will visualize the menu
            - speed - how fast the character should move on the screen
            - x_pos - the X position to spawn the character
            - y_pos - the Y postiion to spawn the character
            - max_lives - the number of lives the player spawns with
            - timeout_seconds - the number of seconds that the player does not take any 
                                damage for when they have been hit by an enemy
            - timeout_seconds - the number of seconds that the player does not take any 
                                damage for and can kill enemies
        """
        
        # Run the __init__ in Character with the given parameters
        super().__init__(path, screen, speed, x_pos, y_pos)
        
        self.max_lives = max_lives
        self.remaining_lives = self.max_lives
        
        self.coins = 0
        self.damage_timeout = 0
        self.powerup_timeout = 0

        # How many seconds you cannot take damage for
        self.damage_timeout_seconds = damage_timeout_seconds
        # How many seconds the pwoerup can last for
        self.powerup_timeout_seconds = powerup_timeout_seconds

        # True means the player has picked up a hat
        self.has_powerup = False


    def damage(self, enemy, timer: int):
        """
        Check if the player has collided with the enemy (taken damage)
        and check if the player is in a "timeout" zone
        """        
        # Check if player and enemy have hit each other
        has_collided = enemy.rect.colliderect(self.rect)
        if not has_collided: return

        if self.has_powerup and has_collided:
            return enemy
        
        # Has the time passed to take new damage => reset self.damage_timeout
        if timer <= self.damage_timeout:
            self.damage_timeout = 0
                
        # Player can take damage => set self.timeout
        # NOTE: the game time starts from a positive number (for example 5 * 60 seconds)
        #       and keeps going down until 0 or a negative number has been reached
        if self.damage_timeout == 0:
            # Can't take damage in the next "timeout_seconds" seconds
            self.damage_timeout = timer - self.damage_timeout_seconds
            # Reduce lives
            self.remaining_lives -= 1

        return None

    def move(self, objects: list, timer: int):
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
        if keys[pygame.K_d] and right_side:
            self.move_right()

        # Move up
        if keys[pygame.K_w] and up_side:
            self.rect.y -= self.speed

        # Move down
        if keys[pygame.K_s] and down_side:
            self.rect.y += self.speed


        to_delete = []
        # Check for collision
        for index in range(len(objects)):
            object = objects[index]

            if object.rect.colliderect(self.rect) and object.name == "bush":
                self.collision(object)

            if object.rect.colliderect(self.rect) and object.name == "coin":
                self.coins += 1
                to_delete.append(index)
            
            if object.rect.colliderect(self.rect) and object.name == "health":
                # Increase the player's health
                if self.remaining_lives < self.max_lives:
                    self.remaining_lives += 1
                    to_delete.append(index)

            if object.rect.colliderect(self.rect) and object.name == "powerup" and not self.has_powerup:
                # Make player immune so they can kill enemies
                self.has_powerup = True
                self.powerup_timeout = timer - self.powerup_timeout_seconds

                to_delete.append(index)

        # Remove picked up coins, health and powerups
        for index in to_delete:
            objects.pop(index)

        # Has the time passed to remove the powerup -> reset self.powerup_timeout
        if timer <= self.powerup_timeout:
            self.has_powerup = False

        # Move the position so there is no lag
        self.screen.blit(self.frame, self.rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)



class Enemy(Character):

    def __init__(self, 
                 path: dict, 
                 screen: pygame.Surface, 
                 index: int,
                 speed: float = 1.4, 
                 x_pos: int = 100, 
                 y_pos: int = 100, 
                 follow_threshold: int = 250, 
                 follow_speed: float = 0.5
                ):
        super().__init__(path, screen, speed, x_pos, y_pos)

        self.follow_threshold = follow_threshold
        self.follow_speed = follow_speed
        self.rng = 0.002
        self.index = index

    def __get_distance(self, player: Player) -> float:
        return math.sqrt((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2)



    def __get_random_number(self) -> float:
        """
        Get a random number between 0 and 1.
        This is required to see if the enemy should 
        move in a direction.
        """
        return round(random.random(), 3)



    def move(self, player: Player, objects: list):
        
        random_move = True

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

        distance = self.__get_distance(player)
        
        in_distance = distance <= self.follow_threshold
        
        left_difference = player.rect.right - self.rect.left
        if (left_difference >= -10 and left_difference <= 50) and in_distance and left_side:
            self.move_left()
            random_move = False

        elif self.__get_random_number() <= self.rng and left_side and random_move:
            self.move_left()
            random_move = False
            
        right_difference = player.rect.left - self.rect.right
        if (right_difference <= 10 and right_difference >= -50) and in_distance and right_side:
            self.move_right()
            
        elif self.__get_random_number() <= self.rng and right_side and random_move:
            self.move_right()
            random_move = False

        up_difference = player.rect.bottom - self.rect.top
        if (up_difference <= 30 and up_difference >= -30) and in_distance and up_side:
            self.rect.y -= self.speed
            random_move = False

        elif self.__get_random_number() <= self.rng and up_side and random_move:
            self.rect.y -= self.speed
            random_move = False

        down_difference = player.rect.top - self.rect.bottom
        if (down_difference <= 30 and down_difference >= -30) and in_distance and down_side:
            self.rect.y += self.speed
            random_move = False
            
        elif self.__get_random_number() <= self.rng and down_side and random_move:
            self.rect.y += self.speed
            random_move = False

        # Check for collision
        for object in objects:
            
            if object.rect.colliderect(self.rect):
                self.collision(object)

        # Move the position so there is no lag
        self.screen.blit(self.frame, self.rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)