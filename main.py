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

sound = pygame.mixer.Sound("sound.mp3")

timer = 0
loading = 0
status = "menu"
running = True
while running:
    for event in pygame.event.get(): # events
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:  # exit with key esc
                running = False

        elif event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN: # click button
            if pygame.mouse.get_pos() >= (150, 230):
                if pygame.mouse.get_pos() <= (250, 280):
                    status = "loading"
                    sound.play()


    pressed_keys = pygame.key.get_pressed()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  # set screen

    if status == "menu":
        pygame.display.set_caption("PATRIK")
        background = pygame.image.load("back.png").convert()
        screen.blit(background, (0, 0))

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
        if timer > 650:
            status = "prepare"
            sound.stop()

    if status == "prepare":
        screen.fill((0, 0, 0))
        loading += 1
        if loading >= 25:
            status = "play"

    if status == "play":
        background = pygame.image.load("play.png").convert()
        screen.blit(background, (0, 0))

    pygame.display.flip()  # update the window
    clock.tick(FPS)

pygame.quit()  # close the window
