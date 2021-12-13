import os
import sys
import time
import pygame
from pygame.locals import *
import Utils as u

# States #
import Start as start
import Moon as moon

pygame.init()
pygame.display.set_caption('Go2DaMoon')
running = True

# Settings / Import from json later? #
FPS = 60
WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)
display = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
GAMEPATH = sys.path[0]
state = [start, moon]
CURRENTSTATE = 0


def main():
    global CURRENTSTATE
    state[CURRENTSTATE].init(pygame, display)
    while running:
        CS = CURRENTSTATE
        deltatime = clock.tick(FPS)
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        CURRENTSTATE = state[CURRENTSTATE].update(pygame, display, deltatime, CS)
        if CS != CURRENTSTATE:
            state[CURRENTSTATE].init(pygame, display)


if __name__ == '__main__':
    u.initassets(pygame)
    main()

