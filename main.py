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


# MINI GAME DINO
def jump():
    global user_y, jump_counter, make_jump
    if jump_counter >= -35:
        user_y -= jump_counter / 2.5
        jump_counter -= 1
        if user_y >= 480:
            user_y = 480
    else:
        jump_counter = 35
        make_jump = False
        if user_y >= 480:
            user_y = 480

# dino in playing
user_x = SCREEN_WIDTH // 4
user_y = SCREEN_HEIGHT - 120

class Cactus:
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
    choice = randint(0, 2)  #first
    img = cactus_image[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]
    array.append(Cactus(SCREEN_WIDTH + 20, height, width, img, 4))

    choice = randint(0, 2)  # second
    img = cactus_image[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]
    array.append(Cactus(SCREEN_WIDTH + 300, height, width, img, 4))

    choice = randint(0, 2)  # third
    img = cactus_image[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]
    array.append(Cactus(SCREEN_WIDTH + 600, height, width, img, 4))

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
            array[i] = (Cactus(SCREEN_WIDTH + 100 + randint(-80, 60), height, width, img, 4))
    return array


BLOCKS = []  # list of bloks for dino
cactus_image = []
cactus_option = [50, 400, 80, 352, 60, 450, 40, 450]

block = pygame.image.load("block.png")
block.set_colorkey((255, 255, 255))
cactus_image.append(block)
block2 = pygame.image.load("block2.png")
block2.set_colorkey((255, 255, 255))
cactus_image.append(block2)
block3 = pygame.image.load("block3.png")
block3.set_colorkey((255, 255, 255))
cactus_image.append(block3)
block4 = pygame.image.load("block4.png")
block4.set_colorkey((255, 255, 255))
cactus_image.append(block4)


BLOCKS = creat_cactus_arr(BLOCKS)

floor_x = 0  # position of ground FOR MOVING

make_jump = False  # DINO jump
jump_counter = 35


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
Status = ["menu", "loading", "prepare", "play", "dino"]
counter = 0
status = Status[counter]

running = True
while running:
    for event in pygame.event.get():  # events
        if event.type == pygame.KEYDOWN:  # events of keyboard
            if event.key == K_ESCAPE:  # exit with key esc
                running = False
            if event.key == pygame.K_RIGHT:  # OPEN NEXT SCENE
                counter += 1
                status = Status[counter]
            if event.key == pygame.K_LEFT:  # OPEN LAST SCENE
                counter -= 1
                status = Status[counter]
            if event.key == pygame.K_SPACE:
                make_jump = True

        elif event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # click button
            if pygame.mouse.get_pos() >= (150, 230):
                if pygame.mouse.get_pos() <= (250, 280):
                    menu_sound.stop()
                    counter += 1
                    status = "loading"
                    sound.play()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  # set screen
    icon = pygame.image.load("icon.png").convert()
    pygame.display.set_icon(icon)

    if status == "menu":
        pygame.display.set_caption("PATRIK")
        background = pygame.image.load("back.png").convert()
        screen.blit(background, (0, 0))
        menu_sound.play()

        start_button = pygame.draw.rect(screen, (0, 0, 240), (150, 90, 100, 50))
        continue_button = pygame.draw.rect(screen, (0, 244, 0), (150, 160, 100, 50))
        quit_button = pygame.draw.rect(screen, (244, 0, 0), (150, 230, 100, 50))

        pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (100, 100), 30)
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
            status = "prepare"

    if status == "prepare":
        screen.fill(ALL_COLORS[4])
        loading += 1
        if loading >= 15:
            sound.stop()
            counter += 1
            status = "play"

    if status == "play":
        background = pygame.image.load("play.png").convert()
        screen.blit(background, (0, 0))
        counter += 1
        status = "dino"

    if status == "dino":
        background = pygame.image.load("play.png").convert()
        screen.blit(background, (0, 0))

        if make_jump == True:
            jump()

        user = pygame.image.load("ufo.png").convert()
        user_rect = user.get_rect(center=(user_x, user_y))
        user.set_colorkey((255, 255, 255))
        screen.blit(user, user_rect)

        draw_array(BLOCKS)

        floor = pygame.image.load("ground.png")
        floor_x -= 4
        screen.blit(floor, (floor_x, 500))
        screen.blit(floor, (floor_x + 800, 500))
        if floor_x <= -800:  # moving ground
            floor_x = 0

    pygame.display.flip()  # update the window
    clock.tick(FPS)

pygame.quit()  # close the window
