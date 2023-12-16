import json
import pygame, sys, random
from pygame.math import Vector2

# Funcție pentru citirea informațiilor din fișierul JSON
def read_settings_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Exemplu de utilizare
file_path = 'settings.json'  # înlocuiește cu calea către fișierul tău JSON
settings = read_settings_from_json(file_path)

# Accesarea dimensiunii tablei
table_width = settings['table_size']['width']
table_height = settings['table_size']['height']
all_obstacles = settings['obstacles']


for key, value in settings.items():
    if key == 'obstacles':
        print(f"{key}:")
        for obstacle in value:
            print(f"  x: {obstacle['x']}, y: {obstacle['y']}")
    else:
        print(f"{key}: {value}")



SCREEN_UPDATE = pygame.USEREVENT

def get_high_score():
        try:
           with open("high_score.txt", "r") as file:
            return int(file.read())
        except FileNotFoundError:
           return 0
def update_high_score(new_score):
         high_score = get_high_score()
         if new_score > high_score:
             with open("high_score.txt", "w") as file:
                file.write(str(new_score))

def get_user_level():
    print("Choose a level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            



class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) -1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)
                

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down
    
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down
    

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

   

class FRUIT:
    def __init__(self, nr_fruits):
        self.fruits = [Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1)) for _ in range(nr_fruits)]

    def draw_fruit(self):
        for fruit in self.fruits:
            x = int(fruit.x * cell_size)
            y = int(fruit.y * cell_size)
            fruit_rect = pygame.Rect(x, y, cell_size, cell_size)
            screen.blit(apple, fruit_rect)

    def randomize(self, index):
        self.fruits[index] = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))

class OBSTACLE:
    def __init__(self, all_obstacles, nr_obstacles):
       

        # Iau primele `nr_obstacles` obstacole din lista completă
        self.obstacles = [Vector2(obstacle["x"], obstacle["y"]) for obstacle in all_obstacles[:nr_obstacles]]

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            x = int(obstacle.x * cell_size)
            y = int(obstacle.y * cell_size)
            obstacle_rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 0, 0), obstacle_rect)



   
class MAIN:
     

    def __init__(self, nr_fruits, all_obstacles, nr_obstacles,level):
       
        self.snake = SNAKE()
        self.fruit = FRUIT(nr_fruits)
        self.obstacle = OBSTACLE(all_obstacles, nr_obstacles)
        self.added=False
        self.level = level

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.obstacle.draw_obstacles()
        self.draw_score()

    def check_collision(self):
        for index, fruit in enumerate(self.fruit.fruits):
            if fruit == self.snake.body[0]:
                self.snake.play_crunch_sound()
                self.fruit.randomize(index)
                self.snake.add_block()
                self.added = False

        for block in self.snake.body[1:]:
            for fruit in self.fruit.fruits:
                if block == fruit:
                    self.fruit.randomize(self.fruit.fruits.index(fruit))

    def check_fail(self):
        current_score = len(self.snake.body) - 3
        best_score = get_high_score()
        # Check if the snake goes out of bounds
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.show_alert("Game Over", f"You lost!   Your score: {current_score}    Best score: {best_score}")
            self.display_game_message("Press R to restart", (screen_size[0] // 2, screen_size[1] // 2)) 
            
            self.game_over()
            start_level_selection()

        # Check if the snake collides with itself or an obstacle
       
        for obstacle in self.obstacle.obstacles:
            if obstacle == self.snake.body[0]:
                self.show_alert("Game Over", f"You lost!   Your score: {current_score}    Best score: {best_score}")
                self.display_game_message("Press R to restart", (screen_size[0] // 2, screen_size[1] // 2)) 

                self.game_over()
                start_level_selection()
    

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

         # Check if the user's score is 5 and add an obstacle and add one more obstacle
        
        if (len(self.snake.body) - 3) > 0:
         if (len(self.snake.body) - 3) % 2 == 0  and self.added == False:
            if len(self.obstacle.obstacles) < len(all_obstacles):
             self.obstacle.obstacles.append(Vector2(all_obstacles[len(self.obstacle.obstacles)]['x'], all_obstacles[len(self.obstacle.obstacles)]['y']))    
         self.added=True 

         keys = pygame.key.get_pressed()
         if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    # Reset the game state and continue
                    self.game_over()
                    self.added = False

    def show_alert(self, title, message):
        alert_background = (255, 0, 0)
        border_color = (0, 0, 0)
        alert_font = pygame.font.Font(None, 36)
        alert_surface = alert_font.render(message, True, (255, 255, 255))
        alert_rect = alert_surface.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

        alert_bg_rect = pygame.Rect(alert_rect.left - 10, alert_rect.top - 10, alert_rect.width + 20, alert_rect.height + 20)
        pygame.draw.rect(screen, alert_background, alert_bg_rect)
        pygame.draw.rect(screen, border_color, alert_bg_rect, 2)

        pygame.draw.rect(screen, (255, 0, 0), alert_rect)
        screen.blit(alert_surface, alert_rect)

        # Adaugă textul "Press Enter to play again" sub mesajul original
        play_again_text = alert_font.render("Press Enter to play again", True, (255, 255, 255))
        play_again_rect = play_again_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + alert_rect.height // 2 + 30))
        screen.blit(play_again_text, play_again_rect)

        play_again_text = alert_font.render("Press CEVA RANDOM", True, (255, 255, 255))
        play_again_rect = play_again_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + alert_rect.height // 2 + 60))
        screen.blit(play_again_text, play_again_rect)

        pygame.display.flip()

        wait_for_key = True
        while wait_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    start_level_selection()
                    wait_for_key = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    start_game(self.level)
                    wait_for_key = False

        # Clear the screen after pressing Enter
        screen.fill((175, 215, 70))
        pygame.display.flip()


    
    def display_game_message(message, position, font_size=20, font_color=(255, 255, 255)):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(message, True, font_color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)

    def game_over(self):
        self.snake.reset()
        #self.return_to_level_selection()

    def return_to_level_selection(self):
        # Afișează un mesaj pentru a indica că poți apăsa Enter pentru a reveni la nivelul de selecție
        return_text = game_font.render("Press Enter to return to level selection", True, (255, 255, 255))
        return_rect = return_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + 50))
        screen.blit(return_text, return_rect)
        pygame.display.flip()

        # Așteaptă până când tasta Enter este apăsată
        wait_for_key = True
        while wait_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    wait_for_key = False
        
    
    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
    

    def draw_score(self):


        score_text = str(len(self.snake.body) - 3)
        update_high_score(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 60)
        score_rect = score_surface.get_rect(center = (score_x,score_y))


        
        # Adapting to display high score
        high_score_value = str(get_high_score())
        high_score_surface = game_font.render(high_score_value, True, (56, 74, 12))
        high_score_rect = high_score_surface.get_rect(center=(score_x, score_y - 700))

        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width+ 6 ,apple_rect.height)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(high_score_surface, high_score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = table_width
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
screen_size = (cell_number * cell_size, cell_number * cell_size)  # Define screen_size
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
button_width = (screen_size[0] // 4)
button_height = (screen_size[1] // 8)
button_spacing = button_height // 6
button_color = (230,0,0)
button_text_color = (255,255,255)


# Function to get the user's level choice
def get_user_level():
    levels = ["Easy", "Medium", "Hard", "Exit"]
    selected_level = None

    buttons = get_buttons_rect(levels)

    while selected_level is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, text in buttons:
                    if button_rect.collidepoint(event.pos):
                        if text == "Exit":
                            selected_level = text
                            # print(text)
                            pygame.quit()
                            sys.exit()
                        else:
                            selected_level = text
                            # pygame.quit()
                            
        screen.fill((175,215,70))
        # button_text = game_font.render("Select Level:", True, (56, 74, 12))
        # screen.blit(button_text, (screen_size[0] // 2 - 100, screen_size[1] // 2 - 50))
        # for i, level in enumerate(levels, start=1):
        #     button_text = game_font.render(f"{i}. {level}", True, (56, 74, 12))
        #     screen.blit(button_text, (screen_size[0] // 2 - 100, screen_size[1] // 2 + i * 30))
        draw_buttons(buttons)

        pygame.display.update()
        clock.tick(60)

    return selected_level

def get_buttons_rect(levels):
    buttons = []
    for i, text in enumerate(levels):
        button_rect = pygame.Rect(
            (screen_size[0] - button_width) // 2,
            (screen_size[1] - (button_height + button_spacing) * len(levels)) // 2 + i * (button_height + button_spacing),
            button_width,
            button_height
        )
        buttons.append((button_rect, text))
    return buttons

def draw_buttons(buttons):
    font_size = int(0.70 * button_height)  # Calculează dimensiunea fontului pe baza înălțimii butonului
    font = pygame.font.Font(None, font_size)
    
    for button_rect, text in buttons:
        pygame.draw.rect(screen, button_color, button_rect, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, border_radius=15, width=3)
        
        button_text = font.render(text, True, button_text_color)
        
        # Ajustează poziția textului pentru a fi în centrul butonului
        text_x = button_rect.centerx - button_text.get_width() // 2
        text_y = button_rect.centery - button_text.get_height() // 2
        screen.blit(button_text, (text_x, text_y))




fruit = FRUIT(0)
snake = SNAKE()
obstacle = OBSTACLE(all_obstacles, 0)


SCREEN_UPDATE =pygame.USEREVENT


def start_game(selected_level):
    if selected_level == "Easy":
        snake_speed = 200
        nr_fruits = 3
        nr_obstacles = 1
    elif selected_level == "Medium":
        snake_speed = 100
        nr_fruits = 2
        nr_obstacles = 2
    else:
        snake_speed = 80
        nr_fruits = 1
        nr_obstacles = 5

    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)

    main_game = MAIN(nr_fruits, all_obstacles, nr_obstacles, selected_level)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if (main_game.snake.direction.y != 1):
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_LEFT:
                    if (main_game.snake.direction.x != 1):
                        main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_DOWN:
                    if (main_game.snake.direction.y != -1):
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_RIGHT:
                    if (main_game.snake.direction.x != -1):
                        main_game.snake.direction = Vector2(1, 0)
        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(90)


def start_level_selection():
    selected_level = get_user_level()
    start_game(selected_level)

start_level_selection()



