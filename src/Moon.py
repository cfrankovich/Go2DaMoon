import sys
import os
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

MAX_HEIGHT = 1958.0 # white
MIN_HEIGHT = -4249.5 # black

MAX_SLOPE = 65.0 # idk
MIN_SLOPE = 0.0 # idk

MOON_IMAGE_NAME = None
MOON_IMG = None

PIXELS = None 


def get_x(lat, latpx):
    return round( (lat-(-89.999))/latpx ) 

def get_y(lon, lonpy, minlon):
    return round( (lon-minlon)/lonpy )

def get_color_efficient(DATA, latpx, lonpy, minlon):
    # loop through data #
    # get x, y from lat, lon #
    # if x, y is a valid coord add to pixels array #
    # once there are SX*SY pixels, break #
    # return pixels #
    pixels = [ [None] * SCREEN_X ] * SCREEN_Y
    totpix = 0
    goal = SCREEN_X * SCREEN_Y
    for line in DATA:
        sp = line.split(',')
        x = get_x(float(sp[0]), latpx)
        y = get_y(float(sp[1]), lonpy, minlon)
        if 0 <= x < SCREEN_X and 0 <= y < SCREEN_Y:
            if pixels[x][y] == None:
                slop = int(sp[3])
                g = int(slop * 3.923077)
                pixels[x][y] = (g, g, g)
                totpix += 1
                print(f'New pixel at [{x}][{y}] :: {totpix}/{goal}')
                if totpix >= goal:
                    break

    print(pixels[20][5])
    pixels[0][5] = (255, 0, 0)
    print(pixels[20][5])

    for i in range(len(pixels)):
        for k in range(len(pixels[i])):
            if pixels[i][k] == None:
                print('green!')
                pixels[i][k] = (0, 255, 0)

    return pixels


def init(pg, display):
    global LAND_LAT
    global LAND_LON
    global DEST_LAT
    global DEST_LON
    global SCREEN_X
    global SCREEN_Y
    global MOON_IMAGE_NAME
    global MOON_IMG
    
    lines = open('TEMPDATA').readlines()
    LAND_LAT = float(lines[0])
    LAND_LON = float(lines[1])
    DEST_LAT = float(lines[2])
    DEST_LON = float(lines[3])
    SCREEN_X = int(lines[4])
    SCREEN_Y = int(lines[5])
    os.remove('TEMPDATA')

    # For the screen #
    MIN_LON = min(LAND_LON, DEST_LON) - 1
    MAX_LON = max(LAND_LON, DEST_LON) + 1 

    latpx = 1.999066 / SCREEN_X
    lonpy = (abs(MAX_LON - MIN_LON)) / SCREEN_Y 

    print('This will take a long time!')
    data = open(f'{sys.path[0]}/../data/lunardata.csv').readlines()
    pixelss = get_color_efficient(data, latpx, lonpy, MIN_LON)
    global PIXELS
    PIXELS = pixelss
    print('Done!')

    arr = np.array(pixelss, dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    MOON_IMAGE_NAME = f'MoonImage_{datetime.now().timestamp()}.png'
    img.save(MOON_IMAGE_NAME)
    MOON_IMG = pg.image.load(f'{sys.path[0]}/{MOON_IMAGE_NAME}').convert()


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
    #display.blit(MOON_IMG, (0, 0))
    # RENDER EACH PIXEL #
    for y, row in enumerate(PIXELS):
        for x, p in enumerate(row):
           display.set_at((x, y), p) 

    # state #
    return cs

