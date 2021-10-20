import pygame
import random, sys, math

from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,
                           RLEACCEL, )  # Import pygame.locals for easier access to key coordinates
from pygame.locals import *
from random import randint
from math import sqrt, pow

pygame.init()  # connect all functions of libruary

# size of display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def print_text(message, x, y, font_color=(0, 0, 0), font_type="PingPong.ttf", font_size=30):
    global screen
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def print_message(message, x, y, font_color=(0, 0, 0), font_type="message.otf", font_size=25):
    global screen
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def print_score(message, x, y, font_color=(0, 0, 0), font_type="score.ttf", font_size=35):
    global screen
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def pause():
    global running
    paused = True
    while paused:
        print_text("Paused. Press Enter to continue...", 160, 300)
        for event in pygame.event.get():  # events
            if event.type == pygame.KEYDOWN:  # events of keyboard
                if event.key == K_ESCAPE:  # exit with key esc
                    paused = False
                    running = False
                if event.key == pygame.K_RETURN:
                    paused = False
            elif event.type == pygame.QUIT:
                paused = False
                running = False
        pygame.display.update()
        clock.tick(15)


# MINI GAME MARIO
tile_size = 30
game_over = 0

class Player():  # CREAT PERSON

    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'guy{num}.png')
            img_right = pygame.transform.scale(img_right, (35, 65))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.dead_image = pygame.image.load('ghost.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def update(self, game_over):

        walk_cooldown = 5
        dx = 0
        dy = 0

        if game_over == 0:

            key = pygame.key.get_pressed()
            if key[pygame.K_j]:
                dx -= 3
                self.counter += 1
                self.direction -= 1
            if key[pygame.K_k]:
                dx += 3
                self.counter += 1
                self.direction = 1
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y -= 11
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.direction = 0
                if self.direction == 1:
                    self.images_right[self.index]
                if self.direction == -1:
                    self.images_left[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.vel_y += 1  # гравитация
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dx= tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                dy = 0

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > -50:
                 self.rect.y -= 5

        screen.blit(self.image, self.rect)
        return game_over


class World():

    def __init__(self, data):
        self.tile_list = []

        dirt_image = pygame.image.load('dirt.png')
        grass_image = pygame.image.load('grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 7)
                    blob_group.add(blob)
                if tile == 7:
                    platform = Platform(col_count * tile_size, row_count * tile_size + 7)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('platform.png')
        self.image = pygame.transform.scale(self.image, (30, 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('blob.png')
        self.image = pygame.transform.scale(self.image, (24, 18))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 25:
            self.move_direction *= -1
            self.move_counter *= -1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
[1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 3, 0, 0, 0, 3, 0, 0, 2, 2, 1],
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6, 1, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player_MARIO = Player(50, SCREEN_HEIGHT - 65)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
world = World(world_data)


# MINI GAME DINO
def jump():
    global user_y, jump_counter, make_jump
    if jump_counter >= -30:
        user_y -= jump_counter / 2.5
        jump_counter -= 1
        if user_y >= 480:
            user_y = 480
    else:
        jump_counter = 30
        make_jump = False
        if user_y >= 480:
            user_y = 480


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -50:
            screen.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            self.x = SCREEN_WIDTH + 100 + randint(-80, 100)
            return False


def creat_cactus_arr(array):
    global cactus_image, cactus_option, SCREEN_WIDTH
    choice = randint(0, 2)  # first
    img = cactus_image[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]
    array.append(Object(SCREEN_WIDTH + 20, height, width, img, 4))

    choice = randint(0, 2)  # second
    img = cactus_image[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]
    array.append(Object(SCREEN_WIDTH + 300, height, width, img, 4))

    choice = randint(0, 2)  # third
    img = cactus_image[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]
    array.append(Object(SCREEN_WIDTH + 600, height, width, img, 4))

    return array


def find_radius(array):
    global SCREEN_WIDTH
    maximum = max(array[0].x, array[1].x, array[2].x)
    radius = 0
    if maximum < SCREEN_WIDTH:
        radius = SCREEN_WIDTH
        if radius - maximum < 50:
            radius += 150
        else:
            radius = maximum

    choice = randint(0, 5)
    if choice == 0:
        radius += randint(10, 15)
    else:
        radius += randint(200, 350)
    return radius


def draw_array(array):
    global cactus_option, cactus_image, SCREEN_WIDTH
    for i in range(3):
        check = array[i].move()
        if not check:
            radius = find_radius(array)

            choice = randint(0, 2)
            img = cactus_image[choice]
            width = cactus_option[choice * 2]
            height = cactus_option[choice * 2 + 1]
            array[i] = (Object(SCREEN_WIDTH + 100 + radius, height, width, img, 4))
    return array


def draw_dino():
    global img_count, user_x, user_y, DINO_img
    if img_count == 25:
        img_count = 0

    screen.blit(DINO_img[img_count // 5], (user_x, user_y))
    img_count += 1


def check_collission(barriers):
    global user_x, user_y, make_jump, jump_counter
    for i in range(3):
        if user_y + 98 >= barriers[i].y:
            if barriers[i] == 450:  # little cactus
                if not make_jump:
                    if barriers[i].x <= user_x + 40 <= barriers[i].x + barriers[i].width:
                        return True
                elif jump_counter >= 0:
                    if user_y + 93 >= barriers[i].y:
                        if barriers[i].x <= user_x + 40 <= barriers[i].x + barriers[i].width:
                            return True
                else:
                    if user_y + 88 >= barriers[i].y:
                        if barriers[i].x <= user_x <= barriers[i].x + barriers[i].width:
                            return True
            else:
                if not make_jump:
                    if barriers[i].x <= user_x + 65 <= barriers[i].x + barriers[i].width:
                        return True
                elif jump_counter == 10:
                    if user_y + 93 >= barriers[i].y:
                        if barriers[i].x <= user_x + 65 <= barriers[i].x + barriers[i].width:
                            return True
                elif jump_counter >= -1:
                    if user_y + 93 >= barriers[i].y:
                        if barriers[i].x <= user_x + 45 <= barriers[i].x + barriers[i].width:
                            return True
                else:
                    if user_y + 88 >= barriers[i].y:
                        if barriers[i].x <= user_x + 5 <= barriers[i].x + barriers[i].width:
                            return True
    return False


def count_cactus(BLOCKS):
    global dino_score
    for i in range(3):
        if BLOCKS[i].x + BLOCKS[i].width < user_x:
            dino_score += 1


blocks = []  # list of bloks for dino
cactus_image = []
cactus_option = [50, 400, 72, 370, 60, 450]

block = pygame.image.load("block.png")
block.set_colorkey((255, 255, 255))
cactus_image.append(block)
block2 = pygame.image.load("block2.png")
block2.set_colorkey((255, 255, 255))
cactus_image.append(block2)
block3 = pygame.image.load("block3.png")
block3.set_colorkey((255, 255, 255))
cactus_image.append(block3)

OBJ_cloud = SCREEN_WIDTH + 10
y_cloud = 80
cloud_img = []
cloud1 = pygame.image.load("sky1.png")
cloud1.set_colorkey((255, 255, 255))
cloud2 = pygame.image.load("sky2.png")
cloud2.set_colorkey((255, 255, 255))
cloud_img.append(cloud1)
cloud_img.append(cloud2)
choice = 0  # change kind of clouds

img_count = 0
DINO_img = [pygame.image.load("Dino0.png"), pygame.image.load("Dino1.png"), pygame.image.load("Dino2.png"),
            pygame.image.load("Dino3.png"), pygame.image.load("Dino4.png")]

# FORTUNE SCENE
fortune_wheel = []
rul_counter = 0
flag = 0
fortune_text = ["YOU WIN! + 1000", "SORRY, -100", "GOOD LUCK! + 50", "NOT AFRAID, - 150", "IT IS SO GOOD, + 10"]
fortune_score = [1000, -100, 50, -150, 10]
message_counter = len(fortune_text)
ruletka1 = pygame.image.load("ruletka.png")  # 1
ruletka1.set_colorkey((255, 255, 255))
ruletka2 = pygame.image.load("ruletka2.png")  # 2
ruletka2.set_colorkey((255, 255, 255))
ruletka3 = pygame.image.load("ruletka3.png")  # 3
ruletka3.set_colorkey((255, 255, 255))
ruletka4 = pygame.image.load("ruletka4.png")  # 4
ruletka4.set_colorkey((255, 255, 255))
fortune_wheel.append(ruletka1)
fortune_wheel.append(ruletka2)
fortune_wheel.append(ruletka3)
fortune_wheel.append(ruletka4)


# FOR LOADING
def buble(x, y, i):
    screen.blit(ALL_BUBLE_IMG[i], (x, y))


ALL_BUBLE_IMG = []
ALL_BUBLEX = []
ALL_BUBLEY = []
ALL_BUBLEX_CHANGE = []
ALL_BUBLEY_CHANGE = []
num_of_bubles = 50

# loading animation
for i in range(num_of_bubles):
    ALL_BUBLE_IMG.append(pygame.image.load("ghost.png"))
    ALL_BUBLEX.append(randint(20, 780))
    ALL_BUBLEY.append(randint(20, 550))
    ALL_BUBLEX_CHANGE.append(5)
    ALL_BUBLEY_CHANGE.append(40)

# BUTONS-PARAMETRS
button1 = pygame.image.load("two_players.png")
button1.set_colorkey((255, 255, 255))
button2 = pygame.image.load("three_players.png")
button2.set_colorkey((255, 255, 255))
button3 = pygame.image.load("fore_players.png")
button3.set_colorkey((255, 255, 255))
on_button = 0

button = pygame.image.load("go_play.png")

kubs = pygame.image.load("kubics.png")

# ALL COLORS
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (255, 0, 255)
ALL_COLORS = [WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN]

FPS = 60  # how often cadrs will change
clock = pygame.time.Clock()

# sounds in game
menu_sound = pygame.mixer.Sound("bells.mp3")
sound = pygame.mixer.Sound("sound.mp3")

# counters of scene
timer = 0
loading = 0
Status = ["menu", "loading", "parametrs", "play", "dino", "fortune", "move_return", "prison", "mario", "bankrupt", "birthday"]
counter = 0
status = Status[counter]
n = 3

prison_score = 0
dino_score = 0

play_game = '34567'
player = 0
num_of_players = 1
list_scores = []
running = True
while running:
    for event in pygame.event.get():  # events
        if event.type == pygame.KEYDOWN:  # events of keyboard
            if event.key == K_ESCAPE:  # exit with key esc
                running = False
            if event.key == pygame.K_RIGHT:  # OPEN NEXT SCENE
                if counter <= 9:
                    counter += 1
                status = Status[counter]
            if event.key == pygame.K_LEFT:  # OPEN LAST SCENE
                counter -= 1
                status = Status[counter]
            if event.key == pygame.K_RETURN:
                pause()
            if counter == 4:
                if event.key == pygame.K_SPACE:
                    make_jump = True
                else:
                    make_jump = False

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # click button
            if pygame.mouse.get_pos() >= (650, 252):
                if pygame.mouse.get_pos() <= (752, 349):
                    if counter == 0:
                        menu_sound.stop()
                        counter += 1
                        status = "loading"
                        sound.play()
            if counter == 2:  # check cursor
                if pygame.mouse.get_pos() >= (390, 180):  # selected 2
                    if pygame.mouse.get_pos() <= (450, 240):
                        num_of_players = 2
                        on_button = 2
                        button1 = pygame.image.load("two_players_pressed.png")
                        button1.set_colorkey((255, 255, 255))
                if pygame.mouse.get_pos() >= (490, 220):  # selected 3
                    if pygame.mouse.get_pos() <= (580, 310):
                        num_of_players = 3
                        on_button = 3
                        button2 = pygame.image.load("three_players_pressed.png")
                        button2.set_colorkey((255, 255, 255))
                if pygame.mouse.get_pos() >= (630, 200):  # selected 4
                    if pygame.mouse.get_pos() <= (690, 260):
                        num_of_players = 4
                        on_button = 4
                        button3 = pygame.image.load("fore_players_pressed.png")
                        button3.set_colorkey((255, 255, 255))

                if pygame.mouse.get_pos() >= (600, 450):
                    if pygame.mouse.get_pos() <= (750, 550):
                        list_scores = []
                        for i in range(num_of_players):
                            list_scores.append(0)
                        player = 0
                        counter += 1
                        status = Status[counter]

            if counter == 3:  # play menu, main map of the game
                if pygame.mouse.get_pos() >= (50, 50):
                    if pygame.mouse.get_pos() <= (170, 120):
                        counter += 1
                        status = "dino"
                if pygame.mouse.get_pos() >= (170, 100):
                    if pygame.mouse.get_pos() <= (290, 170):
                        counter += 2
                        status = "fortune"
                if pygame.mouse.get_pos() >= (130, 170):
                    if pygame.mouse.get_pos() <= (220, 280):
                        counter += 3
                        status = "move_return"
                if pygame.mouse.get_pos() >= (220, 170):
                    if pygame.mouse.get_pos() <= (290, 310):
                        counter += 4
                        status = "prison"

                if pygame.mouse.get_pos() >= (30, 470):  # push cubics, get game
                    if pygame.mouse.get_pos() <= (130, 570):
                        flag = 0
                        if n >= 9:
                            n = 3
                            counter = 3
                        else:
                            n += 1
                        status = Status[n]

                if flag == 1:  # when the message of fortune
                    if pygame.mouse.get_pos() >= (250, 250):
                        if pygame.mouse.get_pos() <= (550, 450):
                            flag = 0
                            if player == num_of_players - 1:
                                player = 0
                            else:
                                player += 1

                if flag == 2:  # when the message of prison
                    if pygame.mouse.get_pos() >= (250, 250):
                        if pygame.mouse.get_pos() <= (550, 450):
                            flag = 0
                            prison_score = 0
                            if player == num_of_players - 1:
                                player = 0
                            else:
                                player += 1

                if flag == 3:  # when the message of dino
                    if pygame.mouse.get_pos() >= (250, 250):
                        if pygame.mouse.get_pos() <= (550, 450):
                            flag = 0
                            list_scores[player] += dino_score
                            dino_score = 0
                            if player == num_of_players - 1:
                                player = 0
                            else:
                                player += 1

                if flag == 4:  # when the message of mario
                    if pygame.mouse.get_pos() >= (250, 250):
                        if pygame.mouse.get_pos() <= (550, 450):
                            flag = 0
                            dino_score = 0
                            if player == num_of_players - 1:
                                player = 0
                            else:
                                player += 1

            if counter == 5:  # the wheel of fortune
                if pygame.mouse.get_pos() >= (200, 150):
                    if pygame.mouse.get_pos() <= (400, 550):
                        counter = 3
                        status = "play"
                        flag = 1
                        vivod = randint(0, message_counter - 1)
                        current_fortune_score = fortune_score[vivod]
                        list_scores[player] += current_fortune_score

            if counter == 6:  # change move to next player
                if pygame.mouse.get_pos() > (0, 0):
                    if pygame.mouse.get_pos() < (800, 600):
                        counter = 3
                        status = Status[counter]
                        if player == num_of_players - 1:
                            player = 0
                        else:
                            player += 1

            if counter == 7:  # exit from prison
                if pygame.mouse.get_pos() >= (prison_x, prison_y):
                    if pygame.mouse.get_pos() <= (prison_x + 30, prison_y + 24):
                        list_scores[player] += prison_score
                        counter = 3
                        status = Status[counter]
                        flag = 2

            if counter == 9:  # bankrupt
                if pygame.mouse.get_pos() >= (0, 0):
                    if pygame.mouse.get_pos() <= (800, 600):
                        list_scores[player] += 0
                        counter = 3
                        status = Status[counter]

            if counter == 10:  # birthday
                if pygame.mouse.get_pos() >= (260, 290):
                    if pygame.mouse.get_pos() <= (520, 555):
                        list_scores[player] += 150 * (num_of_players - 1)
                        for i in range(num_of_players):
                            if i != player:
                                list_scores[i] -= 150
                        counter = 3
                        status = Status[counter]
                        flag = 5

        if counter == 2:  # check cursor
            if pygame.mouse.get_pos() >= (390, 180):  # selected 2
                if pygame.mouse.get_pos() <= (450, 240):
                    if on_button != 2:
                        button1 = pygame.image.load("two_players_click.png")
                        button1.set_colorkey((255, 255, 255))
                else:
                    if on_button != 2:
                        button1 = pygame.image.load("two_players.png")
                        button1.set_colorkey((255, 255, 255))
            else:
                if on_button != 2:
                    button1 = pygame.image.load("two_players.png")
                    button1.set_colorkey((255, 255, 255))

            if pygame.mouse.get_pos() >= (490, 220):  # selected 3
                if pygame.mouse.get_pos() <= (580, 310):
                    if on_button != 3:
                        button2 = pygame.image.load("three_players_click.png")
                        button2.set_colorkey((255, 255, 255))
                else:
                    if on_button != 3:
                        button2 = pygame.image.load("three_players.png")
                        button2.set_colorkey((255, 255, 255))
            else:
                if on_button != 3:
                    button2 = pygame.image.load("three_players.png")
                    button2.set_colorkey((255, 255, 255))

            if pygame.mouse.get_pos() >= (630, 200):  # selected 4
                if pygame.mouse.get_pos() <= (690, 260):
                    if on_button != 4:
                        button3 = pygame.image.load("fore_players_click.png")
                        button3.set_colorkey((255, 255, 255))
                else:
                    if on_button != 4:
                        button3 = pygame.image.load("fore_players.png")
                        button3.set_colorkey((255, 255, 255))
            else:
                if on_button != 4:
                    button3 = pygame.image.load("fore_players.png")
                    button3.set_colorkey((255, 255, 255))

            if pygame.mouse.get_pos() >= (600, 450):
                if pygame.mouse.get_pos() <= (750, 550):
                    button = pygame.image.load("go_play_click.png")
                else:
                    button = pygame.image.load("go_play.png")
            else:
                button = pygame.image.load("go_play.png")

        if counter == 3:
            if pygame.mouse.get_pos() >= (30, 470):  # push cubics, get random game
                if pygame.mouse.get_pos() <= (130, 570):
                    kubs = pygame.image.load("kubics_click.png")
                else:
                    kubs = pygame.image.load("kubics.png")
            else:
                kubs = pygame.image.load("kubics.png")

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  # set screen
    icon = pygame.image.load("icon.png").convert()
    pygame.display.set_icon(icon)

    if status == "menu":
        pygame.display.set_caption("PATRIK")
        background = pygame.image.load("back.png").convert()
        screen.blit(background, (0, 0))
        menu_sound.play()

        button = pygame.image.load("pusk.png")
        screen.blit(button, (650, 252))

        pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (100, 100), 30)  # gosts
        pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (700, 500), 30)
        pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (700, 100), 30)
        pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (100, 500), 30)
        pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (150, 320), 30)
        pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (500, 50), 30)
        pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (530, 530), 30)
        pygame.time.wait(30)

    if status == "loading":
        background = pygame.image.load("background.png").convert()
        screen.blit(background, (0, 0))
        timer += 1

        for i in range(num_of_bubles):
            ALL_BUBLEX[i] += ALL_BUBLEX_CHANGE[i]
            ALL_BUBLEY[i] += ALL_BUBLEY_CHANGE[i]
            if ALL_BUBLEX[i] <= 0:
                ALL_BUBLEX_CHANGE[i] = randint(2, 6)
                ALL_BUBLEX[i] += ALL_BUBLEX_CHANGE[i]
                ALL_BUBLEY_CHANGE[i] = -randint(2, 6)
                ALL_BUBLEY[i] += ALL_BUBLEY_CHANGE[i]
            elif ALL_BUBLEX[i] >= 750:
                ALL_BUBLEX_CHANGE[i] = -randint(2, 6)
                ALL_BUBLEX[i] += ALL_BUBLEX_CHANGE[i]
                ALL_BUBLEY_CHANGE[i] = randint(2, 6)
                ALL_BUBLEY[i] += ALL_BUBLEY_CHANGE[i]
            if ALL_BUBLEY[i] <= 0:
                ALL_BUBLEY_CHANGE[i] = randint(2, 6)
                ALL_BUBLEY[i] += ALL_BUBLEY_CHANGE[i]
                ALL_BUBLEX_CHANGE[i] = randint(2, 6)
                ALL_BUBLEX[i] += ALL_BUBLEX_CHANGE[i]
            elif ALL_BUBLEY[i] >= 550:
                ALL_BUBLEY_CHANGE[i] = -randint(2, 6)
                ALL_BUBLEY[i] += ALL_BUBLEY_CHANGE[i]
                ALL_BUBLEX_CHANGE[i] = -randint(2, 6)
                ALL_BUBLEX[i] += ALL_BUBLEX_CHANGE[i]
            buble(ALL_BUBLEX[i], ALL_BUBLEY[i], i)

        if timer > 500:
            counter += 1
            status = "parametrs"

    if status == "parametrs":
        background = pygame.image.load("parametrs.png")
        screen.blit(background, (0, 0))
        title = "PLAYING OPTIONS"
        print_message(title, 120, 50, font_size=45)
        option = "number of players:"
        print_message(option, 50, 200)

        screen.blit(button1, (390, 180))
        screen.blit(button2, (490, 220))
        screen.blit(button3, (630, 200))

        screen.blit(button, (600, 450))

    if status == "play":
        background = pygame.image.load("play.png").convert()
        screen.blit(background, (0, 0))
        start_dino = pygame.image.load("first.png")
        screen.blit(start_dino, (50, 50))
        start_fortune = pygame.image.load("second.png")
        screen.blit(start_fortune, (170, 100))
        start_return = pygame.image.load("third.png")
        screen.blit(start_return, (130, 170))
        start_prison = pygame.image.load("forth.png")
        screen.blit(start_prison, (220, 170))
        start_mario = pygame.image.load("fiveth.png")
        screen.blit(start_mario, (290, 110))
        start_bunkrupt = pygame.image.load("sixth.png")
        screen.blit(start_bunkrupt, (420, 100))
        start_birthday = pygame.image.load("seventh.png")
        screen.blit(start_birthday, (400, 300))
        start_logik = pygame.image.load("eighth.png")
        screen.blit(start_logik, (480, 230))


        score_message = pygame.image.load("score.png")
        score_message.set_colorkey((255, 255, 255))
        screen.blit(score_message, (550, 20))
        print_message('player ' + str(player + 1), 400, 70)
        print_score(str(list_scores[player]), 600, 70)

        screen.blit(kubs, (30, 470))

        prison_x = randint(0, 800)
        prison_y = randint(0, 600)

        # dino in playing
        BLOCKS = creat_cactus_arr(blocks)
        user_x = SCREEN_WIDTH // 4
        user_y = SCREEN_HEIGHT - 198
        make_jump = False  # DINO jump
        jump_counter = 30
        floor_x = 0  # position of ground FOR MOVING

        if flag == 1:  # print message from fortune
            fortune_message = pygame.image.load("fortune_message.png")
            screen.blit(fortune_message, (250, 250))
            current_fortune_score = fortune_score[vivod]
            print_message(str(fortune_text[vivod]), 280, 300)

        if flag == 2:  # print message from prison
            prison_message = pygame.image.load("prison_message.png")
            screen.blit(prison_message, (250, 250))
            print_message("SORRY, YOU LOSE ", 280, 300)
            print_message(str(prison_score), 320, 350)

        if flag == 3:  # print message from dino
            prison_message = pygame.image.load("dino_message.png")
            screen.blit(prison_message, (250, 250))
            print_message("CONGRATULATIONS!", 280, 300)
            print_message("YOU GOT ", 310, 320)
            print_message(str(dino_score), 350, 350)

        if flag == 4:  # game over message from mario
            mario_message = pygame.image.load("mario_message.png")
            screen.blit(mario_message, (250, 250))
            print_message("you lose 200", 300, 350)

        if flag == 5:  # message from birthday
            pass


    if status == "dino":
        background = pygame.image.load("play.png").convert()
        screen.blit(background, (0, 0))
        print_message(('your score: ' + str(dino_score)), 10, 30)

        if make_jump == True:
            jump()

        draw_dino()

        BLOCKS = draw_array(BLOCKS)
        count_cactus(BLOCKS)

        floor = pygame.image.load("ground.png")
        floor_x -= 4
        screen.blit(floor, (floor_x, 500))
        screen.blit(floor, (floor_x + 800, 500))
        if floor_x <= -800:  # moving ground
            floor_x = 0

        image_cloud = cloud_img[choice]
        if OBJ_cloud >= -120:
            screen.blit(image_cloud, (OBJ_cloud, y_cloud))
            OBJ_cloud -= 2
        else:
            OBJ_cloud = SCREEN_WIDTH + 40 + randint(-30, 50)
            y_cloud = randint(50, 250)
            choice = 1

        if check_collission(BLOCKS):
            flag = 3
            status = 'play'
            counter = 3

    if status == "fortune":
        counter = 5
        flag = 0
        background = pygame.image.load("fortune.png")
        screen.blit(background, (0, 0))
        screen.blit(fortune_wheel[rul_counter // 5], (200, 150))
        rul_counter += 1
        if rul_counter >= 19:
            rul_counter = 0

    if status == "move_return":
        counter = 6
        background = pygame.image.load("change_move.png")
        screen.blit(background, (0, 0))

    if status == "prison":
        counter = 7
        prison_score -= 3
        background = pygame.image.load("prison.png")
        screen.blit(background, (0, 0))
        prison_exit = pygame.image.load("go_out.png")
        screen.blit(prison_exit, (prison_x, prison_y))

    if status == "mario":
        counter = 8
        background = pygame.image.load("mario.png")
        screen.blit(background, (0, 0))
        world.draw()

        if game_over == 0:
            blob_group.update()
            platform_group.update()
        else:
            if player_MARIO.rect.y < -30:
                list_scores[player] -= 200
                counter = 3
                status = "play"
                flag = 4


        blob_group.draw(screen)
        lava_group.draw(screen)
        platform_group.draw(screen)

        game_over = player_MARIO.update(game_over)

    if status == 'bankrupt':
        counter = 9
        background = pygame.image.load("bankrupt.png")
        screen.blit(background, (0, 0))

    if status == "birthday":
        counter = 10
        background = pygame.image.load("birthday.png")
        screen.blit(background, (0, 0))


    pygame.display.flip()  # update the window
    clock.tick(FPS)

pygame.quit()  # close the window
