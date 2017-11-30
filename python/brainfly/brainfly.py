from collections import defaultdict
import sys

import pygame
from pygame.locals import *

ENEMY_SPAWN_TIME = 5000

screen = pygame.display.set_mode((960, 600), DOUBLEBUF)
clock = pygame.time.Clock()
keys = defaultdict(bool)

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, screen_rect, left=True):
        super().__init__()
        self.image = pygame.image.load('ship.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image = pygame.transform.rotate(self.image, 180)
        self.position = [screen_rect.left+50 if left else screen_rect.right-50, screen_rect.top]
        self.screen_rect = screen_rect
    
    def update(self):
        self.position[1] += 1
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        if self.position[1] > self.screen_rect.bottom+50:
            self.kill()

class ShipSprite(pygame.sprite.Sprite):
    def __init__(self, screen_rect):
        super().__init__()
        self.image = pygame.image.load('ship.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.position = list(screen_rect.center)
        self.position[1] = screen_rect.h - 50

    def update(self, keys):
        if keys[K_RIGHT]:
            self.position[0] += 1
        if keys[K_LEFT]:
            self.position[0] -= 1
        self.rect = self.image.get_rect()
        self.rect.center = self.position

rect = screen.get_rect()
ship = ShipSprite(rect)
ship_group = pygame.sprite.RenderPlain(ship)
enemy_group = pygame.sprite.RenderPlain()
last_enemy_spawned = -ENEMY_SPAWN_TIME
left = True

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        keys[event.key] = down
    screen.fill((0, 0, 0))

    # check if an enemy needs to spawn
    time = pygame.time.get_ticks()
    if time - last_enemy_spawned > ENEMY_SPAWN_TIME:
        enemy_group.add(EnemySprite(rect, left))
        left = not left
        last_enemy_spawned = time

    enemy_group.update()
    ship_group.update(keys)
    ship_group.draw(screen)
    enemy_group.draw(screen)
    pygame.display.flip()