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

latpx = 0.0
lonpy = 0.0

MAX_HEIGHT = 1958.0 # idk 
MIN_HEIGHT = -4249.5 # idk 
MAX_SLOPE = 65.0 # whtie 
MIN_SLOPE = 0.0 # black 

MOON_IMAGE_NAME = None
MOON_IMG = None
PIXELS = None 

POINTS = []


def plot_point_ll(pygame, display, lat, lon, r, c):
    x = get_x(lat, latpx) 
    y = get_y(lon, lonpy, MIN_LON) 
    pygame.draw.circle(display, c, (x, y), r)


def plot_point_img(display, lat, lon, i):
    x = get_x(lat, latpx) 
    y = get_y(lon, lonpy, MIN_LON) 
    display.blit(u.ASSETS[i], (x-16, y-16))


def get_avg_color(parr, i, k):
    if i == 0 or i >= SCREEN_X-1:
        return (0, 0, 0)
    elif k == 0 or k >= SCREEN_Y-1:
        return (0, 0, 0)
    s = 0
    s += parr[i-1][k-1][0] 
    s += parr[i-1][k][0] 
    s += parr[i-1][k+1][0] 
    s += parr[i][k-1][0] 
    s += parr[i][k+1][0] 
    s += parr[i+1][k-1][0] 
    s += parr[i+1][k][0] 
    s += parr[i+1][k+1][0] 
    g = s/8
    return (int(g), int(g), int(g)) 


def get_x(lat, latpx):
    return round( (lat-(-89.999))/latpx ) 

def get_y(lon, lonpy, minlon):
    return round( (lon-minlon)/lonpy )


def set_bar(per):
    per = int(per/10)
    bar = ''
    for i in range(per):
        bar += '#'
    for i in range(10-per):
        bar += ' '
    return bar 


def get_color_efficient(DATA, latpx, lonpy, minlon):
    print('[o] Initializing array')
    parr = [[]] * SCREEN_X
    for y in range(SCREEN_X):
        parr[y] = [(0, 255, 0)] * SCREEN_Y

    bar = ''
    print('[o] Reading and processing lunar data')
    print('0% [          ]', end='\r')

    totpix = 0
    goal = SCREEN_X * SCREEN_Y
    for line in DATA:
        sp = line.split(',')
        x = get_x(float(sp[0]), latpx)
        y = get_y(float(sp[1]), lonpy, minlon)
        if 0 <= x < SCREEN_X and 0 <= y < SCREEN_Y:
            if parr[x][y] == (0, 255, 0):
                slop = int(sp[3])
                g = int(slop * 3.923077)
                parr[x][y] = (g, g, g)
                totpix += 1
                per = int((totpix/goal) * 100) 
                bar = set_bar(per)
                print(f'{per}% [{bar}]', end='\r')
                if totpix >= goal:
                    break

    print(f'100% [##########]')
            
    print('[o] Filling in missing values')
    for i in range(len(parr)):
        for k in range(len(parr[i])):
            if parr[i][k] == (0, 255, 0):
                parr[i][k] = get_avg_color(parr, i, k) 
                pass

    return parr


def init(pg, display, argv):
    global LAND_LAT
    global LAND_LON
    global DEST_LAT
    global DEST_LON
    global SCREEN_X
    global SCREEN_Y
    global MOON_IMAGE_NAME
    global MOON_IMG

    print('')
    pi = None
    verbose = False
    for i in range(len(argv)):
        if argv[i] == '-i':
            try:
                pi = argv[i+1]
            except:
                print('[-] Error! No argument given')
        elif argv[i] == '-v' or argv[i] == '--verbose':
            verbose = True
   
    if verbose:
        print('[o] Loading data from temp file')
    lines = open('TEMPDATA').readlines()
    LAND_LAT = float(lines[0])
    LAND_LON = float(lines[1])
    DEST_LAT = float(lines[2])
    DEST_LON = float(lines[3])
    SCREEN_X = int(lines[4]) 
    SCREEN_Y = int(lines[5]) 
    if verbose:
        print('[+] Data loaded! Deleting temp file...')
    os.remove('TEMPDATA')
    if verbose:
        print('[+] Temp file removed')

    # For the screen #
    if verbose:
        print('[o] Calculating crucial data...')
    global MIN_LON
    global MAX_LON
    MIN_LON = min(LAND_LON, DEST_LON) - 1 
    MAX_LON = max(LAND_LON, DEST_LON) + 1 

    global latpx
    global lonpy
    latpx = 1.999066 / SCREEN_X
    lonpy = (abs(MAX_LON - MIN_LON)) / SCREEN_Y 

    if verbose:
        print('[o] Checking for preset image...')
    if pi:
        print('[o] Preset image detected! Skipping rendering process...')
        try:
            MOON_IMG = pg.image.load(pi)
            print('[o] Preset image loaded!')
            return
        except:
            print('[-] Error loading image!')
    
    print('[o] Rendering image...')
    data = open(f'{sys.path[0]}/../data/lunardata.csv').readlines()
    pixelss = get_color_efficient(data, latpx, lonpy, MIN_LON)
    global PIXELS
    PIXELS = pixelss
    print('[+] Done!')

    if verbose:
        print('[o] Saving image to file')
    arr = np.array(pixelss, dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    MOON_IMAGE_NAME = f'MoonImage_{LAND_LAT}_{LAND_LON}_{DEST_LAT}_{DEST_LON}.png'
    img.save(MOON_IMAGE_NAME)
    MOON_IMG = pg.image.load(f'{sys.path[0]}/{MOON_IMAGE_NAME}').convert()
    if verbose:
        print('[+] Image successfully saved!')


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
    display.fill((0, 255, 0))
    display.blit(MOON_IMG, (0, 0))

    # Now plot the two points #
    plot_point_img(display, LAND_LAT, LAND_LON, 2)
    plot_point_img(display, DEST_LAT, DEST_LON, 1)

    # state #
    return cs

