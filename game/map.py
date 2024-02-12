import pygame
from game.character import Character

class Object:

    def __init__(self, path: str, screen: pygame.Surface, x_pos: int, y_pos: int) -> None:
        """
        Visualize a single objects on the map
        """
        self.screen = screen
        self.image = pygame.image.load(path).convert_alpha()
        # Make image exact size
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    
    def collision(self, character: Character):
        
        if not self.rect.colliderect(character.rect): return

        if self.rect.right > character.rect.left and self.rect.left < character.rect.left:
            print("Right")

        elif self.rect.left < character.rect.right and self.rect.right > character.rect.right:
            print("Left")

        elif self.rect.bottom > character.rect.top and self.rect.top < character.rect.top:
            print("Bottom")

        elif self.rect.top < character.rect.bottom and self.rect.bottom > character.rect.bottom:
            print("Top")



    def draw(self):
        self.screen.blit(self.image, self.rect)

    @property
    def width(self):
        """
        Create a variable called width
        """
        return self.image.get_width()

    @property
    def height(self):
        """
        Create a variable called height
        """
        return self.image.get_height()


class Map:

    def __init__(self, paths: str, map_data: list, screen: pygame.Surface, x_increment: int = 50, y_increment: int = 50, x_start_value: int = 25, y_start_value: int = 25):
        """
        Draw the map for the level
        """ 
        self.map_data = map_data
        self.x_increment = x_increment
        self.y_increment = y_increment

        self.x_start_value = x_start_value
        self.y_start_value = y_start_value

        self.__game_map = []
        self.__screen = screen

        # Insert objects in here
        self.__my_objects = {
            "bush": lambda x_pos, y_pos: Object(paths["bush"], self.__screen, x_pos, y_pos)
        }

    
    def create(self):
        """
        Get the X and Y coordinates of the map objects
        """
        x = self.x_start_value
        y = self.y_start_value

        for rows in self.map_data:

            for cell in rows:
                obj = self.__my_objects.get(cell)
                if obj:
                    self.__game_map.append(obj(x, y))

                x += self.x_increment

            x = self.x_start_value        
            y += self.y_increment



    def collide(self, character: Character):
        """
        Draw all of the items on the map
        """
        for item in self.__game_map:
            
            item.collision(character)
            item.draw()
