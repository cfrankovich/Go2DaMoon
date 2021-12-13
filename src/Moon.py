import sys
from PIL import Image
from datetime import datetime
import numpy as np
import Utils as u

LAND_LAT = 0.0 
LAND_LON = 0.0 
DEST_LAT = 0.0 
DEST_LON = 0.0 
SCREEN_X = 0
SCREEN_Y = 0

MIN_LAT = -89.999067 # left  
MAX_LAT = -88.000001 # right 
MIN_LON = 0.0 # top
MAX_LON = 0.0 # bottom

def init(pg):
    global LAND_LAT
    global LAND_LON
    global DEST_LAT
    global DEST_LON
    global SCREEN_X
    global SCREEN_Y
    
    lines = open('TEMPDATA').readlines()
    LAND_LAT = float(lines[0])
    LAND_LON = float(lines[1])
    DEST_LAT = float(lines[2])
    DEST_LON = float(lines[3])
    SCREEN_X = int(lines[4])
    SCREEN_Y = int(lines[5])

    # For the screen #
    MIN_LON = min(LAND_LON, DEST_LON) - 1
    MAX_LON = max(LAND_LON, DEST_LON) + 1 

    # Six dec. places #
    pixels = []
    latpx = 1.999066 / SCREEN_X
    lonpy = (abs(MAX_LON - MIN_LON)) / SCREEN_Y 

    for py in range(SCREEN_Y):
        row = []
        for px in range(SCREEN_X):
            # find out color and add to row
            row.append((0, 255, 0))
        pixels.append(row)

    arr = np.array(pixels, dtype=np.uint8)
    img = Image.fromarray(arr)
    img.save('MoonImage_{datetime.now()}.png')

    pg.display.set_mode((SCREEN_X, SCREEN_Y), 0)


def update(pygame, display, deltatime, cs):
    # tick #
    pressed = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events: 
            if event.type == 256:
                print('Exiting...')
                pygame.quit()
                sys.exit()

    # render #
    display.fill((19, 27, 35))

    # state #
    return cs

