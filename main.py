import pygame
import random
import sys

from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,
                           RLEACCEL, )  # Import pygame.locals for easier access to key coordinates
from pygame.locals import *
from random import randint

pygame.init()  # connect all functions of libruary


def buble(x, y, i):
    screen.blit(ALL_BUBLE_IMG[i], (x, y))


def jump():
    global user_y
    global jump_counter
    global make_jump
    if jump_counter >= -30:
        user_y -= jump_counter // 2.5
        jump_counter -= 1
        if user_y >= 400:
            user_y = 400
    else:
        jump_counter = 30
        make_jump = False
        if user_y >= 400:
            user_y = 400



# size of display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# dino in playing
user_width = 60
user_height = 100
user_x = SCREEN_WIDTH // 4
user_y = 400

cactus_width = 20
cactus_height = 70
cactus_x = SCREEN_WIDTH - 50
cactus_y = SCREEN_HEIGHT - cactus_height - 100
num_of_cactus = 7
all_cactus = []


make_jump = False
jump_counter = 30

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

FPS = 70  # how often cadrs will change
clock = pygame.time.Clock()

# sounds in game
menu_sound = pygame.mixer.Sound("bells.mp3")
sound = pygame.mixer.Sound("sound.mp3")

ALL_BUBLE_IMG = []
ALL_BUBLEX = []
ALL_BUBLEY = []
ALL_BUBLEX_CHANGE = []
ALL_BUBLEY_CHANGE = []
num_of_bubles = 40

# loading animation
for i in range(num_of_bubles):
    image = pygame.image.load("ghost.png")
    ALL_BUBLE_IMG.append(image)
    ALL_BUBLEX.append(randint(20, 780))
    ALL_BUBLEY.append(randint(20, 550))
    ALL_BUBLEX_CHANGE.append(5)
    ALL_BUBLEY_CHANGE.append(40)

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
            buble(ALL_BUBLEX[i], ALL_BUBLEY[i], i)
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

        pygame.draw.rect(screen, (ALL_COLORS[5]), (user_x, user_y, user_width, user_height))

        if cactus_x >= -cactus_width:
            pygame.draw.rect(screen, (255, 255, 255), (cactus_x, cactus_y, cactus_width, cactus_height))
            cactus_x -= 4
        else:
            cactus_x = SCREEN_WIDTH - 50



    pygame.display.flip()  # update the window
    clock.tick(FPS)

pygame.quit()  # close the window
