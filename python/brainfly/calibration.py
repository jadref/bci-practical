from collections import defaultdict
import sys
import time
sys.path.append('../signalProc')

import numpy as np

import pygame
from pygame.locals import *

import bufhelp
from util import intlist

RESOLUTION = (960, 600)
ELLIPSIS = np.array([0.2, 0.15])
BACKGROUND_COLOR = (42, 42, 42)
GAME_TIME = 90
EPOCH_DURATION = 4.5


class Ellipse:

    def __init__(self, position, size, color=(100, 100, 100), text=''):
        self.position = np.array(position)
        self.size = np.array(size) * screen_rect[1]
        self.text = text
        self.color = color

    def draw(self, screen):
        rect = intlist(np.concatenate([self.position*screen_rect-self.size/2, self.size]))
        pygame.draw.ellipse(screen, self.color, rect)
        text = font.render(self.text, True, [255, 255, 255])
        screen.blit(text, (rect[0]+text.get_rect().w, rect[1]+text.get_rect().h))


screen = pygame.display.set_mode(RESOLUTION, DOUBLEBUF | NOFRAME)
pygame.init()
screen_rect = screen.get_rect()
screen_rect = np.array([screen_rect.w, screen_rect.h])
font = pygame.font.Font(pygame.font.get_default_font(), int(screen_rect[1]*0.05))
# bufhelp.connect()
clock = pygame.time.Clock()
keys = defaultdict(bool)

lasttime = last_swap = time.time()
sides = ['L', 'R']*20
left = Ellipse([0.1, 0.5], [0.2, 0.15], text='LH')
right = Ellipse([0.9, 0.5], [0.2, 0.15], text='RH')
middle = Ellipse([0.5, 0.5], [0.1, 0.1])
i = 0
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

    if curtime - last_swap >= EPOCH_DURATION:
        i += 1
        last_swap = curtime
        if sides[i] == 'L':
            left.color = [0, 255, 0]
            right.color = [100, 100, 100]
        else:
            left.color = [100, 100, 100]
            right.color = [0, 255, 0]
    screen.fill(BACKGROUND_COLOR)

    left.draw(screen)
    right.draw(screen)
    middle.draw(screen)


    pygame.display.flip()
    if i == len(sides):
        sys.exit()
