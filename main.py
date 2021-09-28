import pygame
import random

from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, RLEACCEL, )  # Import pygame.locals for easier access to key coordinates
from pygame.locals import *

pygame.init()  # connect all functions of libruary


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 5)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("PATRIK")
    background = pygame.image.load("back.png")
    screen.blit(background, (0, 0))


    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)


    if pygame.sprite.spritecollideany(player, enemies): # Check if any enemies have collided with the player
        player.kill()
        running = False

    pygame.display.flip()  # update the window
    clock.tick(FPS)

pygame.quit()  # close the window
