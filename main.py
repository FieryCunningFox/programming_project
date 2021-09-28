import pygame
import random
import sys

from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, RLEACCEL, )  # Import pygame.locals for easier access to key coordinates
from pygame.locals import *
from random import randint

pygame.init()  # connect all functions of libruary


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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

FPS = 70 # how often cadrs will change
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:  # exit with key esc
                running = False

        elif event.type == pygame.QUIT:
            running = False


    pressed_keys = pygame.key.get_pressed()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # set screen
    pygame.display.set_caption("PATRIK")
    background = pygame.image.load("back.png").convert()
    screen.blit(background, (0, 0))

    pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (100, 100), 30)
    pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (700, 500), 30)
    pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (700, 100), 30)
    pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (100, 500), 30)
    pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (150, 320), 30)
    pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (500, 50), 30)
    pygame.draw.circle(screen, (ALL_COLORS[randint(0, 7)]), (530, 530), 30)
    pygame.time.wait(30)

    pygame.display.flip()  # update the window
    clock.tick(FPS)

pygame.quit()  # close the window
