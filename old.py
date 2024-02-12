# imports 
import pygame
import time
import sys
import random
import math

# initalise pygame
pygame.init()

#create display window and assign the images for the buttons to variables to be loaded later on
screen_height = 729
screen_width = 728
menu_image = "simply_london.PNG"
play_image = "play_menu_button.PNG"
highscore_image = "high_score_button.PNG"
control_image = "controls_button.PNG"
quit_image = "quit_game_button.PNG"
# tiles for maps variables
grass_tile = "bush_for_map.PNG"
map_background = "map_backgroundfm.PNG"

# map resolution
map_width = 729
map_height = 729

# barriers
barrier_x = 623
barrier_y = 624

# define font
font = pygame.font.SysFont("arialblack", 58)
# define second font
font_two = pygame.font.SysFont("arialblack", 35)

#define enemy width and height (may need to be changed)
enemy_width = 50 
enemy_height = 50  

# define clock to set the refresh rate of the screen
clock = pygame.time.Clock()

# define colours
text_colour = (255,255,255)
# define back button colour
back_button_colour = (100,100,100)  

# set up the display for the game and the caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tory Tangle") 

# load the menu image
menu_img = pygame.image.load(menu_image).convert_alpha()
#load button images
play_img = pygame.image.load(play_image).convert_alpha()
highscore_img = pygame.image.load(highscore_image).convert_alpha()
control_img = pygame.image.load(control_image).convert_alpha()
quit_img = pygame.image.load(quit_image).convert_alpha()

# Load custom tiles
grass_tile = pygame.image.load("bush_for_map.PNG").convert_alpha()
map_background = pygame.image.load("map_backgroundfm.PNG")

# button class
class Button:
    # make the button images load in
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect(center=position)
    # draw the button images on the screen
    def draw(self):
        screen.blit(self.image, self.rect)
    # check if the buttons have been clicked 
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# define back button rectangle 
back_button_rect = pygame.Rect(20, screen_height - 80, 100, 50)  

# Function to display the high score screen
def show_high_score_screen():
    # Creates a new screen for the high score screen
    high_score_screen = pygame.Surface((screen_width, screen_height))
    # draw the screen black
    high_score_screen.fill((0, 0, 0)) 

    # Draw a white square at the top of the high score screen
    box_rect = pygame.Rect(50, 50, screen_width - 100, 100)
    pygame.draw.rect(high_score_screen, (255, 255, 255), box_rect)

    # Display "High Scores" in red inside the white box at the top of the high score screen
    high_score_caption = font.render("High Scores", True, (255, 0, 0))
    high_score_caption_rect = high_score_caption.get_rect(center=(screen_width // 2, 100))
    high_score_screen.blit(high_score_caption, high_score_caption_rect)

    # The 5 High Scores (CHANGE LATER)
    high_scores = [9000, 8000, 7000, 6000, 5000]

    # Spacing of the high scores
    score_spacing = 80
    starting_y = 200

    # Display the 5 high scores on the High Score screen
    for i, score in enumerate(high_scores):
        score_text = font.render(f"{i + 1}. {score}", True, (0, 255, 0))
        score_rect = score_text.get_rect(center=(screen_width // 2, starting_y + i * score_spacing))
        high_score_screen.blit(score_text, score_rect)

    # Draw a back button on the bottom left of the High Score screen
    back_button_rect = pygame.Rect(20, screen_height - 80, 100, 50)
    pygame.draw.rect(high_score_screen, back_button_colour, back_button_rect)
    back_button_text = font.render("Back", True, text_colour)
    back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
    high_score_screen.blit(back_button_text, back_button_text_rect)

    # Blit the high score screen onto the main display
    screen.blit(high_score_screen, (0, 0))
    pygame.display.update() 

# Function to display the controls on the screen
def show_controls_screen():
    controls_screen = pygame.Surface((screen_width, screen_height))
    controls_screen.fill((0, 0, 0))
# set the caption Controls at the top of the screen in blues
    controls_caption = font.render("Controls", True, (0, 0, 255))
    controls_caption_rect = controls_caption.get_rect(center=(screen_width // 2, 50))
    controls_screen.blit(controls_caption, controls_caption_rect)
# controls for the game
    controls_text = [
        "W - Move Forward",
        "A - Move Left",
        "S - Move Down",
        "D - Move Right",
        "E - Activate Power Up",
        "Left Mouse Button - Shoot Gun",
        "Esc - To pause and unpause the game"
    ]
# space out the text
    text_spacing = 80
    starting_y = 150
# display the controls on the screen
    for i, control in enumerate(controls_text):
        control_text = font_two.render(control, True, (255, 255, 255))
        control_rect = control_text.get_rect(center=(screen_width // 2, starting_y + i * text_spacing))
        controls_screen.blit(control_text, control_rect)
# create a button at the bottom left of the screen
    back_button_rect = pygame.Rect(20, screen_height - 80, 100, 50)
    pygame.draw.rect(controls_screen, back_button_colour, back_button_rect)
    back_button_text = font.render("Back", True, text_colour)
    back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
    controls_screen.blit(back_button_text, back_button_text_rect)

    screen.blit(controls_screen, (0, 0))
    pygame.display.update()

# Define game_screen at the global level
game_screen = None
# Create a dictonary to store different tile types
tile_types = {
    "grass": pygame.image.load("bush_for_map.PNG").convert_alpha(),
}

# fuction to show the game screen
def show_game_screen():
    # global variable for the game_screen 
    global game_screen 

    # create a new surface for the game screen
    game_screen = pygame.Surface((map_width, map_height))
    # draw the screen black
    game_screen.fill((0, 0, 0)) 

    # draw the map background onto the game screen
    game_screen.blit(map_background, (0, 0))    

    # Map with custom tiles (needs to be changed)
    map_data = [
        [None, None, None, None, None, None, None, None, None, "grass", "grass", None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, "grass", "grass", None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "grass", None, "grass", None, None, None, None, None, None, None, None, None, "grass", None, "grass", None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, "grass", None, None, None, None, None, None, None, None, None, "grass", None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, "grass", "grass", "grass", "grass", None, None, None, None, None, None, None, None, None, None],
        [None, "grass", "grass", "grass", None, None, None, None, None, None, None, None, None, None, None, None, "grass", "grass", "grass", None, None, None],
        [None, "grass", "grass", "grass", None, None, None, None, None, None, None, None, None, None, None, None, "grass", "grass", "grass", None, None, None],
        [None, None, None, None, None, None, "grass", None, None, None, None, None, None, "grass", None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, "grass", None, None, None, None, None, None, "grass", None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, "grass", None, None, None, None, None, None, "grass", None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, "grass", None, None, None, None, None, None, "grass", None, None, None, None, None, None, None, None],
        [None, "grass", "grass", "grass", None, None, None, None, None, None, None, None, None, None, None, None, "grass", "grass", "grass", None, None, None],
        [None, "grass", "grass", "grass", None, None, None, None, None, None, None, None, None, None, None, None, "grass", "grass", "grass", None, None, None],
        [None, None, None, None, None, None, None, None, "grass", "grass", "grass", "grass", None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, "grass", None, None, None, None, None, "grass", None, None, None, None, None, None, None, None],
        [None, None, "grass", None, "grass", None, None, None, None, None, None, None, None, None, None, "grass", None, "grass", None, None, None, None],
        [None, None, None, None, None, None, None, None, None, "grass", "grass", None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, "grass", "grass", None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ]

    # size of the tile
    tile_size = 30 

    #calculate the start position to center the tiles on the map
    start_x = (map_width - len(map_data[0]) * tile_size) // 2
    start_y = (map_height - len(map_data) * tile_size) // 2

# nested for loop to position the tiles on the map and check if the co - ordinate is valid or not to be placed on the map
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            tile_type = map_data[row][col]
            if tile_type is not None:
                tile = tile_types.get(tile_type)
                if tile is not None:
                    tile_rect = tile.get_rect(topleft=(start_x + col * tile_size, start_y + row * tile_size))
                    game_screen.blit(tile, tile_rect)

    # set barrier to ensure the player cannot move beyond the barrier (623 x 624) - (map to be played on) this resolution is the barrier that the player can't move of the map
    barrier_x = 623
    barrier_y = 624
    player.rect.x = min(max(player.rect.x, 0), barrier_x - player.rect.width)
    player.rect.y = min(max(player.rect.y, 0), barrier_y - player.rect.height)

    # draw the game screen onto the main display
    screen.blit(game_screen, (0, 0))
    pygame.display.update()

    # function to set a specific tile at a given position
def set_tile(row,col,tile_type):
    map_data[row][col] = tile_type

    #set tile at specific position
    set_tile(1, 1, "grass")

    # Calculate the starting position to center the tiles on the map
    start_x = (map_width - len(map_data[0]) * tile_size) // 2
    start_y = (map_height - len(map_data) * tile_size) // 2

    # nested for loop to retirve the tiles and place them on the map
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            tile_type = map_data[row][col]
            if tile_type is not None:
                tile = tile_types.get(tile_type)  # Retrieve the tile from the dictionary
                if tile is not None:
                    tile_rect = tile.get_rect(topleft=(start_x + col * tile_size, start_y + row * tile_size))
                    game_screen.blit(tile, tile_rect)

    # draw the game screen onto the main display
    screen.blit(game_screen, (0, 0))
    pygame.display.update()    


    # timer on the play game screen for 5 seconds
def countdown_timer():
    global game_state  # Use the global game state variable

    countdown_time = 5  # 5 seconds countdown
    while countdown_time:
        show_game_screen()  # Draw the game screen first
        countdown_text = font.render(str(countdown_time), True, text_colour)
        text_rect = countdown_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(countdown_text, text_rect)
        pygame.display.update(text_rect)  # Update only the area of the countdown timer
        time.sleep(1)  # Wait for one second
        countdown_time -= 1

    time.sleep(1.3)  # Wait for 1.3 seconds after the countdown
    game_state = STATE_PLAYING  # Change the game state to playing


   # create the player sprite 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("borisjohnson.sprite.PNG").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        #loads the idle sprite for the after moving right
        self.idle_sprite = pygame.image.load("borisjohnson.sprite.PNG").convert_alpha() 
        #loads the idle sprite for the after moving left
        self.idle_left_sprite = pygame.image.load("borisidle.leftsprite.PNG").convert_alpha()  

        #loads the sprites animation for moving up or right
        self.sprites_right_up = [
            pygame.image.load("borisjohnson.sprite_mr1.PNG").convert_alpha(),
            pygame.image.load("borisjohnson.sprite_mr2.PNG").convert_alpha(),
            pygame.image.load("borisjohnson.sprite_mr3.PNG").convert_alpha()
        ]

        #loads the sprites animation for moving left or down
        self.sprites_left_down = [
            pygame.image.load("borisjohnson.sprite_ml1.PNG").convert_alpha(),
            pygame.image.load("borisjohnson.sprite_ml2.PNG").convert_alpha(),
            pygame.image.load("borisjohnson.sprite_ml3.PNG").convert_alpha()
        ]

        #checks if the last movement was to the left
        self.last_move_left = False    
        #sets the player sprite moving right or up.
        self.current_sprites = self.sprites_right_up
        self.current_frame = 0
        # sets player sprite as idle
        self.image = self.idle_sprite 
        self.rect = self.image.get_rect(center=(x, y))
        # sets player sprite animation speed and how fast the character moves
        self.speed = 1.4
        self.animation_speed = 0.13
        self.frame_count = 0
# updates player sprite when a key is pressed
    def update(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_w]: # up movement
            self.current_sprites = self.sprites_right_up
            self.rect.y -= self.speed
            moved = True
        if keys[pygame.K_s]: # down movement
            self.current_sprites = self.sprites_left_down
            self.rect.y += self.speed
            moved = True
        if keys[pygame.K_a]: # left movement
            self.current_sprites = self.sprites_left_down
            self.rect.x -= self.speed
            moved = True
            self.last_move_left = True  #sets the last move to left
        if keys[pygame.K_d]: # right movement
            self.current_sprites = self.sprites_right_up
            self.rect.x += self.speed
            moved = True
            self.last_move_left = False  # doesn't set last move to the left


        #define buffer for collision boundary
        buffer = 5

        #collision boundaries to be centered on the middle of the map
        barrier_left = (map_width - barrier_x) / 5 + buffer
        barrier_top = (map_height - barrier_y) / 2 + buffer
        barrier_right = barrier_left + barrier_x - buffer * -10
        barrier_bottom = barrier_top + barrier_y - buffer * 0

        # makes the player only allowed to move within the collision boundary and can't move beyond the collision boundary
        self.rect.x = max(barrier_left, min(self.rect.x, barrier_right - self.rect.width))
        self.rect.y = max(barrier_top, min(self.rect.y, barrier_bottom - self.rect.height))

        # handles player sprite animation
        if moved:
            self.frame_count += self.animation_speed
            if self.frame_count >= len(self.current_sprites):
                self.frame_count = 0
            self.current_frame = int(self.frame_count)
            self.image = self.current_sprites[self.current_frame]
        else:
            if self.last_move_left:
                self.image = self.idle_left_sprite  # idle left sprite used if the last move was left
            else:
                self.image = self.idle_sprite  # else normal idle sprite is used
            self.frame_count = 0
# draw player sprite onto the screen
    def draw(self):
        screen.blit(self.image, self.rect)
        
# 4 enemy sprites
# m or f after enemy reprsents if it's a male or female enemy sprite
enemy_m_sprite = pygame.image.load("rndenemym.sprite.PNG").convert_alpha()
enemy_f_sprite = pygame.image.load("rndenemyw.sprite.PNG").convert_alpha()
enemytwo_m_sprite = pygame.image.load("rndenemym.spritetwo.PNG").convert_alpha()
enemytwo_f_sprite = pygame.image.load("rndenemyw.spritetwo.PNG").convert_alpha()
# easter egg enemies
rishisunak_enemy_sprite = pygame.image.load("rishisunak.sprite.PNG").convert_alpha()
liztruss_enemy_sprite = pygame.image.load("liztruss.sprite.PNG").convert_alpha()

# bomb sprite
bomb_sprite = pygame.image.load("bomb.sprite.PNG").convert_alpha()

# enemy sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = random.choice(['up', 'down', 'left', 'right'])  # Randomly choose initial direction
        self.speed = random.uniform(0.6, 1)  # Random speed between 0.6 and 1.0
        self.set_new_direction()
        self.change_time = 0  # Timer to track when to change direction

    def set_new_direction(self):
        # Randomly select horizontal and vertical directions
        horizontal = random.choice(['left', 'right', None])
        vertical = random.choice(['up', 'down', None])
        self.direction = (horizontal, vertical)

    def get_distance_to_player(self, player):
        return math.sqrt((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2)

    def update(self,player):
        distance_to_player = self.get_distance_to_player(player)
        follow_threshold = 40  # will only chase the enemy within these number of steps, if increased will be larger distance so will be difficult to chase if reduced will be smaller distance so will be more easier to chase 
        lose_threshold = 44  # Distance at which enemy stops following
        follow_chance = 0.40    # 40% chance to follow the player when within range
        if distance_to_player < follow_threshold and random.random() < follow_chance:
            # Reduced speed when following the player
            follow_speed = 0.5
            # Move towards the player
            if self.rect.centerx < player.rect.centerx:
                self.rect.x += follow_speed
            elif self.rect.centerx > player.rect.centerx:
                self.rect.x -= follow_speed
            if self.rect.centery < player.rect.centery:
                self.rect.y += follow_speed
            elif self.rect.centery > player.rect.centery:
                self.rect.y -= follow_speed
        else:
        # Move the enemy based on the direction
            if self.direction[0] == 'left':
                self.rect.x -= self.speed
            elif self.direction[0] == 'right':
                self.rect.x += self.speed
            if self.direction[1] == 'up':
                self.rect.y -= self.speed
            elif self.direction[1] == 'down':
                self.rect.y += self.speed
        
        # Change direction at regular intervals
        self.change_time += 1
        if self.change_time > 30:  # Change direction every 30 frames for quicker changes
            self.set_new_direction()
            self.change_time = 0

        #define buffer for collision boundary
        buffer = 5

        #collision boundaries to be centered on the middle of the map
        barrier_left = (map_width - barrier_x) / 5 + buffer
        barrier_top = (map_height - barrier_y) / 2 + buffer
        barrier_right = barrier_left + barrier_x - buffer * -10
        barrier_bottom = barrier_top + barrier_y - buffer * 0

        # makes the enemy only allowed to move within the collision boundary and can't move beyond the collision boundary
        self.rect.x = max(barrier_left, min(self.rect.x, barrier_right - self.rect.width))
        self.rect.y = max(barrier_top, min(self.rect.y, barrier_bottom - self.rect.height))
    
    # draw enemy
    def draw(self):
        screen.blit(self.image, self.rect)

# Define bomb sprite class
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

        #define buffer for collision boundary
        buffer = 5

        #collision boundaries to be centered on the middle of the map
        barrier_left = (map_width - barrier_x) / 5 + buffer
        barrier_top = (map_height - barrier_y) / 2 + buffer
        barrier_right = barrier_left + barrier_x - buffer * -10
        barrier_bottom = barrier_top + barrier_y - buffer * 0

        # makes the bomb only allowed to move within the collision boundary and can't move beyond the collision boundary
        self.rect.x = max(barrier_left, min(self.rect.x, barrier_right - self.rect.width))
        self.rect.y = max(barrier_top, min(self.rect.y, barrier_bottom - self.rect.height))

    # Draw the bomb
    def draw(self):
        screen.blit(self.image, self.rect)

# Function to create a bomb at a random position within barriers
def create_random_bomb():
    bomb_width, bomb_height = bomb_sprite.get_size()
    x = random.randint(0, barrier_x - bomb_width)
    y = random.randint(0, barrier_y - bomb_height)
    return Bomb(x, y, bomb_sprite)

# Initialize bomb to None
bomb = None

# Set the fixed positions for each enemy at the corners of the map
enemy_m_sprite_position = (100, 100)                               # Top left
enemy_f_sprite_position = (map_width - enemy_width - 50, 100)     # Top right
enemytwo_m_sprite_position = (100, map_height - enemy_height - 50)   # Bottom left
enemytwo_f_sprite_position = (map_width - enemy_width - 50, map_height - enemy_height - 50)  # Bottom right

# create enemy instances
enemy_m_sprite = Enemy(*enemy_m_sprite_position, enemy_m_sprite)
enemy_f_sprite = Enemy(*enemy_f_sprite_position, enemy_f_sprite)
enemytwo_m_sprite = Enemy(*enemytwo_m_sprite_position, enemytwo_m_sprite)
enemytwo_f_sprite = Enemy(*enemytwo_f_sprite_position, enemytwo_f_sprite)

# creation of button objects
play_button = Button(play_img, (screen_width // 2, screen_height // 4))
highscore_button = Button(highscore_img, (screen_width // 2, screen_height // 2.75 + 70))
control_button = Button(control_img, (screen_width // 2, screen_height // 2.15 + 140))
quit_button = Button(quit_img, (screen_width // 2, screen_height // 1.75 + 210))

# create a player instance
player = Player(map_width//2, map_height//2)

# creation of bomb instance outside the game loop
bomb = None

# main menu loop
run = True
show_high_score_screen_flag = False
show_controls_screen_flag = False
play_game_flag = False
while run:
    # if event is quit the program will close and the program will stop running
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False
            pygame.quit()
            sys.exit()

            # if mouse button is clicked the position of the mouse will be returned
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # checks if play button is clicked
            if play_button.is_clicked(mouse_pos):
                print("Play button clicked")
                # Set the flag to transition to the game
                play_game_flag = True
                # Change the screen dimensions to 728x729
                map_width = 728
                map_height = 729
                screen = pygame.display.set_mode((screen_width, screen_height))

            # checks if highscore button is clicked
            elif highscore_button.is_clicked(mouse_pos):
                print("High Score button clicked")
                # set the flag to show the high score screen
                show_high_score_screen_flag = True  

            # checks if controls button is clicked
            elif control_button.is_clicked(mouse_pos):
                print("Controls button clicked")    
                show_controls_screen_flag = True  

            # checks if quit button is clicked
            elif quit_button.is_clicked(mouse_pos):
                print("Quit button clicked")
                run = False
            
    # Draw the menu image on the screen
    screen.blit(menu_img, (0, 0))

    # set Tory Tangle as a caption on the top of the screen
    text = font.render("Tory Tangle",True,text_colour)
    text_rect = text.get_rect(center=(screen_width // 2, 50))
    screen.blit(text, text_rect)

    # display and position the button images on the screen
    playimage_rect = play_img.get_rect(center=(screen_width // 2, screen_height //4))
    highscoreimage_rect = highscore_img.get_rect(center=(screen_width // 2, screen_height // 2.75 + 70))
    controlimage_rect = control_img.get_rect(center=(screen_width // 2, screen_height // 2.15 + 140))
    quit_image_rect = quit_img.get_rect(center=(screen_width // 2, screen_height // 1.75 + 210))

    # draw the button images on the main menu
    screen.blit(play_img, playimage_rect)
    screen.blit(highscore_img,highscoreimage_rect)
    screen.blit(control_img,controlimage_rect)
    screen.blit(quit_img,quit_image_rect)

    # Update the display
    pygame.display.update()

    # show the high score screen if the flag is set
    if show_high_score_screen_flag:
        show_high_score_screen()

        # run a different loop for the high score screen to stay displayed until back button is pressed
        high_score_loop = True
        while high_score_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    high_score_loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                # Check if the back button is clicked
                if back_button_rect.collidepoint(mouse_pos):
                        show_high_score_screen_flag = False
                        high_score_loop = False

            pygame.display.update()

    # Run a separate loop for the Controls screen to keep it displayed
    elif show_controls_screen_flag:
        show_controls_screen()
        controls_loop = True
        while controls_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    controls_loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button_rect.collidepoint(mouse_pos):
                        show_controls_screen_flag = False
                        controls_loop = False
            pygame.display.update()

    # Show game screen if the flag is set
    elif play_game_flag:
        # Display the game screen
        show_game_screen()  

        # Create a player instance in the middle of the map
        player = Player(map_width // 2, map_height // 2)

        # Reset the flag after transitioning to the game
        play_game_flag = False

        # Run a separate loop for the game/map screen to keep it displayed
        game_loop = True
        while game_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_loop = False

            player.update() # update player movement based on keyboard input

            # Update the position and direction of each enemy
            enemy_m_sprite.update(player)
            enemy_f_sprite.update(player)
            enemytwo_m_sprite.update(player)
            enemytwo_f_sprite.update(player)

            # Blit the map background onto the main display
            screen.blit(map_background, (0, 0))

            # Draw enemies
            enemy_m_sprite.draw()
            enemy_f_sprite.draw()
            enemytwo_m_sprite.draw()
            enemytwo_f_sprite.draw()

             #map with custom tiles (need to be changed)
            map_data = [
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ]

            # tile size 
            tile_size = 30 

            # Calculate the starting position to center the tiles on the map
            start_x = (map_width - len(map_data[0]) * tile_size) // 2
            start_y = (map_height - len(map_data) * tile_size) // 2

            # nested for loop to keep the map displayed and the position of the tiles on the map
            for row in range(len(map_data)):
                for col in range(len(map_data[row])):
                    tile_type = map_data[row][col]
                    if tile_type is not None:
                        tile = tile_types.get(tile_type)
                        tile_rect = tile.get_rect(topleft=(start_x + col * tile_size, start_y + row * tile_size))
                        screen.blit(tile, tile_rect)

            # Draw enemies and bomb
            enemy_m_sprite.draw()
            enemy_f_sprite.draw()
            enemytwo_m_sprite.draw()
            enemytwo_f_sprite.draw()

            # Bomb creation and drawing logic
            if bomb is None:
                bomb = create_random_bomb()
            bomb.draw()

            # update and draw the player
            screen.blit(game_screen, (0, 0))
            player.draw()

           # Draw enemies
            enemy_m_sprite.draw()
            enemy_f_sprite.draw()
            enemytwo_m_sprite.draw()
            enemytwo_f_sprite.draw()
            bomb.draw()
            pygame.display.update()
            clock.tick(60)

# Reset the game flags after exiting the game loop
        play_game_flag = False
        bomb = None

# Quit pygame and exit the program
pygame.quit()
sys.exit()