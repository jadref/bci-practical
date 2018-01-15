from collections import defaultdict
import sys
import time
sys.path.append('../signalProc')

import numpy as np

import pygame
from pygame.locals import *

import bufhelp
from util import intlist, lerp

RESOLUTION = (960, 600)
ELLIPSIS = np.array([0.2, 0.15])
BACKGROUND_COLOR = (42, 42, 42)
GAME_TIME = 90
JUMP_DURATION = 0.5
EPOCH_DURATION = 4.5
BETWEEN_DURATION = 1.5
PAUSE_TIME = 16


class Ellipse:

    def __init__(self, position, size, color=(100, 100, 100), text=''):
        self.position = np.array(position)
        self.size = np.array(size) * screen_rect[1]
        self.text = text
        self.color = color
        self.offset = np.zeros(2)

    def draw(self, screen):
        rect = intlist(np.concatenate([(self.position+self.offset)*screen_rect-self.size/2, self.size]))
        pygame.draw.ellipse(screen, self.color, rect)
        text = font.render(self.text, True, [255, 255, 255])
        text_x, text_y = intlist(self.position*screen_rect)
        screen.blit(text, [text_x - text.get_rect().width//2, text_y - text.get_rect().height//2])


screen = pygame.display.set_mode(RESOLUTION, DOUBLEBUF | NOFRAME)
pygame.init()
screen_rect = screen.get_rect()
screen_rect = np.array([screen_rect.w, screen_rect.h])
font = pygame.font.Font(pygame.font.get_default_font(), int(screen_rect[1]*0.05))
bufhelp.connect()
clock = pygame.time.Clock()
keys = defaultdict(bool)

lasttime = last_swap = last_jump = stim_end_time = time.time()
in_epoch = False
sides = [''] + ['L', 'R']*20
left = Ellipse([0.1, 0.5], [0.2, 0.15], text='LH')
right = Ellipse([0.9, 0.5], [0.2, 0.15], text='RH')
middle = Ellipse([0.5, 0.5], [0.1, 0.1])
i = 0
bufhelp.sendEvent('stimulus.training', 'start')
middle_offset_goal = middle_start_pos = 0
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

    if not in_epoch and curtime - stim_end_time >= BETWEEN_DURATION:
        i += 1
        if i % PAUSE_TIME == 1:
            pause_text = font.render('Break time! Press any key when you are ready to continue', True, [255, 255, 255])
            center_x, center_y = screen.get_rect().center
            text_width, text_height = pause_text.get_rect().size
            screen.blit(pause_text, [center_x-text_width//2, center_y-text_height//2])
            pygame.display.flip()
            while not any(hasattr(e, 'key') and e.type == KEYDOWN for e in pygame.event.get()):
                time.sleep(0.1)
        last_swap = curtime
        if i == len(sides)-1:
            bufhelp.sendEvent('stimulus.training', 'end')
            sys.exit()
        if sides[i] == 'L':
            left.color = (119, 221, 119)
            right.color = (100, 100, 100)
            middle.text = 'LH'
        else:
            left.color = (100, 100, 100)
            right.color = (119, 221, 119)
            middle.text = 'RH'
        middle.color = (119, 221, 119)

        bufhelp.sendEvent('stimulus.target', 1 if sides[i] == 'R' else 0)
        in_epoch = True

    if in_epoch and curtime - last_swap >= EPOCH_DURATION:
        middle.text = ''
        left.color = right.color = (100, 100, 100)
        middle.color = (255, 105, 97)
        stim_end_time = curtime
        in_epoch = False
    screen.fill(BACKGROUND_COLOR)

    if curtime - last_jump >= JUMP_DURATION:
        last_jump = curtime
        middle_offset_goal = np.random.normal(0, 0.005, 2)
        middle_start_pos = middle.offset

    middle.offset = lerp(middle_start_pos, middle_offset_goal, (curtime - last_jump) / JUMP_DURATION)

    left.draw(screen)
    right.draw(screen)
    middle.draw(screen)
    progress_text = font.render(f'{i}/{len(sides)-1}', True, [255, 255, 255])
    screen.blit(progress_text, [0, 0])

    pygame.display.flip()
