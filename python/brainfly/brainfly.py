from collections import defaultdict
import sys
import time

import numpy as np
import pygame
from pygame.locals import *

RESOLUTION = (960, 600)
BACKGROUND_COLOR = (42, 42, 42)

ENEMY_MIN_SIZE = 0.05
ENEMY_MAX_SIZE = 0.5
ENEMY_ALIVE_TIME = 9
ENEMY_SPAWN_TIME = ENEMY_ALIVE_TIME / 2
ENEMY_SPEED = 1 / ENEMY_ALIVE_TIME

PLAYER_SPEED = 0.3

screen = pygame.display.set_mode(RESOLUTION, DOUBLEBUF | NOFRAME)
screen_rect = screen.get_rect()
screen_rect = np.array([screen_rect.w, screen_rect.h])
clock = pygame.time.Clock()
keys = defaultdict(bool)

def intlist(array):
    return np.around(array).astype(int).tolist()

class EnemySprite(pygame.sprite.Sprite):
    GROWTH_RATE = (ENEMY_MAX_SIZE / ENEMY_MIN_SIZE)**(1/ENEMY_ALIVE_TIME)

    def __init__(self, left=True):
        super().__init__()
        self.image = pygame.image.load('ship.png')
        self.left = left
        self.scale = np.array([ENEMY_MIN_SIZE, ENEMY_MIN_SIZE])
        self.image = pygame.transform.scale(self.image, intlist(self.scale*screen_rect))
        self.image = pygame.transform.rotate(self.image, 180)
        self.original_image = self.image
        xpos = (0.0 + self.scale[0]*0.5) if left else (1 - self.scale[0] * 0.5)
        self.position = np.array([xpos, 0.0])
        self.spawntime = time.time()
    
    def update(self, deltatime):
        self.position[1] += ENEMY_SPEED * deltatime
        time_elapsed = time.time() - self.spawntime
        scale = self.scale * self.GROWTH_RATE**time_elapsed
        self.image = pygame.transform.scale(self.original_image, intlist(scale*screen_rect))
        self.position[0] = ENEMY_MIN_SIZE / 2 * self.GROWTH_RATE**time_elapsed
        if not self.left:
            self.position[0] = 1- self.position[0]
        self.rect = self.image.get_rect()
        self.rect.center = intlist(self.position * screen_rect)
        if self.rect.bottom > RESOLUTION[1]:
            self.kill()

class ShipSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ship.png')
        self.scale = np.array([0.1, 0.1])
        self.image = pygame.transform.scale(self.image, intlist(self.scale*screen_rect))
        self.position = np.array([0.5, 1]) - self.scale * 0.5

    def update(self, deltatime, keys):
        if keys[K_RIGHT]:
            self.position[0] += PLAYER_SPEED * deltatime
        if keys[K_LEFT]:
            self.position[0] -= PLAYER_SPEED * deltatime
        self.rect = self.image.get_rect()
        self.rect.center = intlist(self.position * screen_rect)

rect = screen.get_rect()
ship = ShipSprite()
ship_group = pygame.sprite.RenderPlain(ship)
enemy_group = pygame.sprite.RenderPlain()
last_enemy_spawned = -ENEMY_SPAWN_TIME
left = True
lasttime = time.time()
while True:
    clock.tick(60)
    curtime = time.time()
    deltatime = curtime - lasttime
    lasttime = curtime
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        keys[event.key] = down
        if event.type == QUIT or keys[K_ESCAPE]:
            sys.exit()
    screen.fill(BACKGROUND_COLOR)

    # check if an enemy needs to spawn
    if curtime - last_enemy_spawned > ENEMY_SPAWN_TIME:
        enemy_group.add(EnemySprite(left))
        left = not left
        last_enemy_spawned = curtime

    rect = screen.get_rect()
    enemy_group.update(deltatime)
    ship_group.update(deltatime, keys)
    ship_group.draw(screen)
    enemy_group.draw(screen)
    pygame.display.flip()