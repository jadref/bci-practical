from collections import defaultdict
import sys

import pygame
from pygame.locals import *

screen = pygame.display.set_mode((960, 600), DOUBLEBUF)
clock = pygame.time.Clock()
keys = defaultdict(bool)

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

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        keys[event.key] = down
    if keys[K_ESCAPE]:
        sys.exit()
    screen.fill((0, 0, 0))
    ship_group.update(keys)
    ship_group.draw(screen)
    pygame.display.flip()