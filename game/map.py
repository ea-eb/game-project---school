import pygame

class Object:

    def __init__(self, path: str, screen: pygame.Surface, x_pos: int, y_pos: int, name: str) -> None:
        """
        Visualize a single objects on the map
        """
        self.name = name
        self.screen = screen
        self.image = pygame.image.load(path).convert_alpha()
        # Make image exact size
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


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

        self.__game_objects = []
        self.__screen = screen

        # Insert objects in here
        self.__paths = paths
        

    
    def create(self):
        """
        Get the X and Y coordinates of the map objects
        """
        x = self.x_start_value
        y = self.y_start_value

        for rows in self.map_data:

            for cell in rows:
                if cell:
                    self.__game_objects.append(
                        Object(self.__paths[cell], self.__screen, x, y, cell)
                    )

                x += self.x_increment

            x = self.x_start_value        
            y += self.y_increment

    
    @property
    def objects(self) -> list:
        """
        Get all of the game objects that are drawn on the screen
        """
        return self.__game_objects

    def draw(self):
        """
        Draw all of the items on the map
        """
        for item in self.__game_objects:
            item.draw()
