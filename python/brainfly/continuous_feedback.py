"""
Continuous feedback phase

Closely resembles the real game, but a lot slower
The player gets reset whenever the next enemy appears
"""
from collections import defaultdict
import sys
import time

import numpy as np
import pygame
from pygame.locals import *

sys.path.append('../signalProc')
import bufhelp
from controller import PlayerController, ProbablisticConroller
from util import intlist, lerp

# Constants for game behaviour
RESOLUTION = (960, 600)
BACKGROUND_COLOR = (42, 42, 42)

ENEMY_MIN_SIZE = 0.05
ENEMY_MAX_SIZE = 0.5
ENEMY_ALIVE_TIME = 9
ENEMY_SPAWN_TIME = ENEMY_ALIVE_TIME + 2
ENEMY_SPEED = 1 / ENEMY_ALIVE_TIME
PREDICTION_TIME = 0.1
GAME_TIME = 90

PLAYER_SPEED = 0.3
BULLET_SPEED = 0.8

# Classes for all the entities in the game
class Bullet(pygame.sprite.Sprite):
    """A bullet is a square that moves up every iteration"""
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface(intlist(screen_rect[1] * np.array([0.03, 0.03])))
        self.image.fill([0, 255, 0])
        self.rect = self.image.get_rect()
        self.position = np.array([x, 0.95])

    def update(self, deltatime):
        self.position[1] -= deltatime * BULLET_SPEED
        self.rect.center = intlist(self.position * screen_rect)


class EnemySprite(pygame.sprite.Sprite):
    """
    Enemies spawn either on the left or the right side of the screen
    They slowly get larger as they move to the bottom
    """
    GROWTH_RATE = (ENEMY_MAX_SIZE / ENEMY_MIN_SIZE) ** (1 / ENEMY_ALIVE_TIME)

    def __init__(self, left=True):
        super().__init__()
        self.image = pygame.image.load('ship.png')
        self.left = left
        self.scale = np.array([ENEMY_MIN_SIZE, ENEMY_MIN_SIZE])
        self.image = pygame.transform.scale(self.image, intlist(self.scale * screen_rect))
        self.image = pygame.transform.rotate(self.image, 180)
        self.original_image = self.image
        r = np.random.uniform(0.8, 0.93)
        xpos = 1 - r if left else r
        self.position = np.array([xpos, 0.0])
        self.spawntime = time.time()

    def update(self, deltatime):
        self.position[1] += ENEMY_SPEED * deltatime
        time_elapsed = time.time() - self.spawntime
        scale = self.scale * self.GROWTH_RATE ** time_elapsed
        self.image = pygame.transform.scale(self.original_image, intlist(scale * screen_rect))
        self.rect = self.image.get_rect()
        self.rect.center = intlist(self.position * screen_rect)
        self.rect.bottom = intlist(self.position * screen_rect)[1]


class ShipSprite(pygame.sprite.Sprite):
    """The player"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ship.png')
        self.scale = np.array([0.1, 0.1])
        self.image = pygame.transform.scale(self.image, intlist(self.scale * screen_rect[0]))
        self.position = np.array([0.5, 0.94])

    def update(self, deltatime, keys):
        if keys[K_RIGHT]:
            self.position[0] += PLAYER_SPEED * deltatime
        if keys[K_LEFT]:
            self.position[0] -= PLAYER_SPEED * deltatime
        self.rect = self.image.get_rect()
        self.rect.center = intlist(self.position * screen_rect)


def draw_enemies(enemies, screen):
    """Draw the enemies and the red line behind them"""
    for enemy in enemies:
        pygame.draw.line(screen, [155, 10, 10], [0, enemy.rect.center[1]], [screen_rect[0], enemy.rect.center[1]], 3)
    enemies.draw(screen)


# Set up the game
screen = pygame.display.set_mode(RESOLUTION, DOUBLEBUF | NOFRAME)
screen_rect = screen.get_rect()
screen_rect = np.array([screen_rect.w, screen_rect.h])
clock = pygame.time.Clock()
keys = defaultdict(bool)
bufhelp.connect()

score = n_shots = n_deaths = n_hits = 0
rect = screen.get_rect()
ship = ShipSprite()
ship_group = pygame.sprite.RenderPlain(ship)
ship_start_pos = 0.5
controller = PlayerController()
enemy_group = pygame.sprite.RenderPlain()
bullet_group = pygame.sprite.RenderPlain()
last_enemy_spawned = -ENEMY_SPAWN_TIME
last_pred_time = 0
left = True
pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 16)
lasttime = last_bullet_spawned = game_start_time = time.time()

bufhelp.sendEvent('experiment.im', 'start')
# Main game loop
while True:
    clock.tick(60)  # 60 FPS
    curtime = time.time()
    deltatime = curtime - lasttime
    lasttime = curtime

    # Record which keys are pressed and check if the game should exit
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        keys[event.key] = down
        if event.type == QUIT or keys[K_ESCAPE]:
            sys.exit()
    screen.fill(BACKGROUND_COLOR)

    # check if an enemy needs to spawn
    if curtime - last_enemy_spawned > ENEMY_SPAWN_TIME:
        bufhelp.sendEvent('stimulus.target', int(not left))  # right is 1
        enemy_group.add(EnemySprite(left))
        left = not left
        last_enemy_spawned = curtime

    if curtime - last_pred_time > PREDICTION_TIME:
        # Ask for a new prediction and process the predictions received
        last_pred_time = curtime
        bufhelp.sendEvent('experiment.predict', 1)
        events = bufhelp.buffer_newevents('classifier.prediction', timeout_ms=0.01)
        for event in events:
            print(f'Got prediction event: {event.value}')
            controller.move(event.value[0])
        ship_start_pos = ship.position[0]

    if curtime - last_bullet_spawned > 1:
        # Spawn a new bullet
        last_bullet_spawned = curtime
        n_shots += 1
        bullet_group.add(Bullet(ship.position[0]))

    # Update all the entities
    enemy_group.update(deltatime)
    ship_group.update(deltatime, keys)
    bullet_group.update(deltatime)

    ship.position[0] = lerp(ship_start_pos, controller.desired_position, (curtime - last_pred_time) / PREDICTION_TIME)

    # Check if any enemies have reached the bottom of the screen
    for enemy in enemy_group:
        if enemy.rect.bottom > screen_rect[1]:
            enemy.kill()
            n_deaths += 1
            ship.position[0] = controller.desired_position = 0.5

    # Check if an enemy has collided with a bullet
    collisions = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)
    for k, v in collisions.items():
        n_hits += 1
        score += int(round(10 * (screen_rect[1] - k.rect.center[1]) / screen_rect[1] + 1))
        ship.position[0] = controller.desired_position = 0.5
        last_enemy_spawned = curtime - ENEMY_SPAWN_TIME

    # Check if a bullet has gone beyond the lowest enemy
    lowest_enemy = max(e.rect.center[1] for e in enemy_group) if enemy_group else 0
    for bullet in bullet_group:
        if bullet.rect.top <= lowest_enemy:
            bullet.kill()

    score_text = font.render(
        f'Shots: {n_shots} | hits: {n_hits} | acc: {n_hits/(n_shots+1e-12):.2f} | '
        f'bonus: {0} out of {1} | Died {n_deaths} times      SCORE: {score}',
        True, [255, 255, 255])
    screen.blit(score_text, (0, 0))

    # Draw everything
    ship_group.draw(screen)
    bullet_group.draw(screen)
    draw_enemies(enemy_group, screen)
    pygame.display.flip()

    if game_start_time + GAME_TIME < curtime:
        # The game is done
        bufhelp.sendEvent('experiment.im', 'end')
        sys.exit()
