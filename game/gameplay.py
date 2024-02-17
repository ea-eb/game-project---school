from game.map import Map
from game.character import Player, Enemy
import constants
import utils
import pygame
import random

class Gameplay:

    def __init__(self, levels: list[list[list]], paths: dict, screen: pygame.Surface, screen_width: int = constants.SCREEN_WIDTH, screen_height: int = constants.SCREEN_HEIGHT):
        """
        The gameplay logic goes in here
        """
        self.screen = screen
        self.__paths = paths

        self.__map_paths = self.__paths["map"]
        
        # All levels
        self.levels = levels
        # Only current level
        self.player = Player(self.__paths["player"], self.screen, 3)

        self.total_level_coins = 0
        self.next_level = 1
        self.final_level = len(self.levels) - 1
        
        self.enemies = []
        self.__total_enemies = 2

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.create_level(self.levels[0])

        self.coins_collected = 0


    def create_level(self, level: list[list]):
        """
        Generate the current level

        Parameters:
            - level - the current level map
        """
        # Reset the player's status
        self.player.coins = 0
        if self.next_level == 1:
            self.player.remaining_lives = self.player.max_lives

        self.total_level_coins = 0
        
        # Count total number of coins
        for row in level:
            for value in  row:
                if value != "coin": continue
                self.total_level_coins += 1

        # Create enemies with random X and Y starting positions
        self.enemies = []

        for index in range(self.__total_enemies):
            
            x_pos = random.randint(100, self.screen_width - 100)
            y_pos = random.randint(100, self.screen_height - 100)
            
            follow_threshold = random.randint(250, 500)
            follow_speed = round(random.uniform(0.5, 1), 2)

            self.enemies.append(
                Enemy(self.__paths["enemy_1"], self.screen, index, x_pos = x_pos, y_pos = y_pos, follow_threshold = follow_threshold, follow_speed = follow_speed)
            )

        self.current_map = Map(self.__map_paths, level, self.screen)
        self.current_map.create()

        self.__total_enemies += 2



    def play(self, timer: int) -> bool:
        """
        The gameplay mechanics.

        Parameters:
            - timer - the remaining time in seconds
        """
        
        # Player has died or there is no more time in the game left
        if self.player.remaining_lives == 0 or timer <= 0:
            utils.save_high_score(self.__paths["menu"]["high_score"], self.coins_collected)
            return False
        
        
        # Player has not collected maximum number of coins in the game
        if self.player.coins < self.total_level_coins:
            self.player.move(self.current_map.objects, timer)

            # Enemies to delete
            to_delete = []
            for enemy in self.enemies:
                remove_enemy = self.player.damage(enemy, timer)
                enemy.move(self.player, self.current_map.objects)

                # Remove enemmies that have been hit while the player has a powerup
                if remove_enemy:
                    self.enemies.remove(remove_enemy)

            
            
        else:
            # Keep track of collected coins
            self.coins_collected += self.player.coins

            # Check if game has finished
            if self.next_level > self.final_level: 
                
                utils.save_high_score(self.__paths["menu"]["high_score"], self.coins_collected)
                return False

            # Go to next level
            self.create_level(self.levels[self.next_level])
            self.next_level += 1
        

        self.current_map.draw()
        return True