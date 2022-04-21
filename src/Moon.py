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

MOON_IMG = None
H_IMG = None
S_IMG = None
PIXELS = None 

board = None
PATH_POINTS = []


def adjust_points():
    pass


def plot_point_ll(pygame, display, x, y, r, c):
    pygame.draw.circle(display, c, (x, y), r)


def plot_point_img(display, x, y, i):
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


def get_x(lat):
    return round( (lat-(-89.999))/latpx ) 

def get_y(lon):
    return round( (lon-MIN_LON)/lonpy )

def get_lat(x):
    return x*latpx + -89.999 

def get_lon(y):
    return y*lonpy + MIN_LON

def set_bar(per):
    per = int(per/10)
    bar = ''
    for i in range(per):
        bar += '#'
    for i in range(10-per):
        bar += ' '
    return bar 

def findpath():
    # A* didnt work out and i have four hours :( #
    global PATH_POINTS
    PATH_POINTS = []
    pass

def get_height_color(h):
    if h >= 924:
        return (224, 31, 31)
    elif h >= -110:
        return (240, 238, 86)
    elif h >= -1144:
        return (42, 172, 48)
    elif h >= -2178:
        return (240, 238, 86)
    elif h >= -3212:
        return (67, 58, 238)
    return (224, 31, 31)

def get_slope_color(s):
    if s >= 20:
        return (224, 31, 31)
    elif s >= 15:
        return (240, 220, 86)
    elif s >= 10:
        return (67, 147, 71)
    elif s >= 5:
        return (42, 172, 48)
    return (113, 254, 120)

def get_color_efficient(DATA, latpx, lonpy, minlon, pg):
    print('[o] Initializing array')

    parr = [[]] * SCREEN_X
    for y in range(SCREEN_X):
        parr[y] = [(0, 255, 0)] * SCREEN_Y

    hpix = [[]] * SCREEN_X
    for y in range(SCREEN_X):
        hpix[y] = [(0, 255, 0)] * SCREEN_Y

    spix = [[]] * SCREEN_X
    for y in range(SCREEN_X):
        spix[y] = [(0, 255, 0)] * SCREEN_Y

    bar = ''
    print('[o] Reading and processing lunar data')
    print('0% [          ]', end='\r')

    totpix = 0
    goal = SCREEN_X * SCREEN_Y
    for line in DATA:
        sp = line.split(',')
        x = get_x(float(sp[0]))
        y = get_y(float(sp[1]))
        if 0 <= x < SCREEN_X and 0 <= y < SCREEN_Y:
            if parr[x][y] == (0, 255, 0):
                slop = int(sp[3])
                g = int(slop * 3.923077)
                parr[x][y] = (g, g, g) # normal
                height = sp[2].replace(' ', '')
                hpix[x][y] = get_height_color(float(height))
                spix[x][y] = get_slope_color(slop)
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

    for i in range(len(hpix)):
        for k in range(len(hpix[i])):
            if hpix[i][k] == (0, 255, 0):
                hpix[i][k] = (0, 0, 0) 
                pass

    for i in range(len(spix)):
        for k in range(len(spix[i])):
            if spix[i][k] == (0, 255, 0):
                spix[i][k] = (0, 0, 0) 
                pass

    arr = np.array(parr, dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    MOON_IMAGE_NAME = f'MoonImage_{LAND_LAT}_{LAND_LON}_{DEST_LAT}_{DEST_LON}.png'
    img.save(MOON_IMAGE_NAME)

    arr = np.array(hpix, dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    img.save('HEIGHT-' + MOON_IMAGE_NAME)

    arr = np.array(spix, dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    img.save('SLOPE-' + MOON_IMAGE_NAME)

    global MOON_IMG
    global H_IMG 
    global S_IMG
    MOON_IMG = pg.image.load(f'{sys.path[0]}/{MOON_IMAGE_NAME}').convert()
    H_IMG = pg.image.load(f'{sys.path[0]}/HEIGHT-{MOON_IMAGE_NAME}').convert() 
    H_IMG.set_alpha(60)
    S_IMG = pg.image.load(f'{sys.path[0]}/SLOPE-{MOON_IMAGE_NAME}').convert() 
    S_IMG.set_alpha(80)

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
            global MOON_IMG
            global H_IMG 
            global S_IMG
            MOON_IMG = pg.image.load(pi)
            H_IMG = pg.image.load('HEIGHT-' + pi)
            H_IMG.set_alpha(60)
            S_IMG = pg.image.load('SLOPE-' + pi)
            S_IMG.set_alpha(80)
            print('[o] Preset image loaded!')
            return
        except:
            print('[-] Error loading image!')
    
    print('[o] Rendering image...')
    data = open(f'{sys.path[0]}/../data/lunardata.csv').readlines()
    pixelss = get_color_efficient(data, latpx, lonpy, MIN_LON, pg)
    print('[+] Done!')

hdisp = False
sdisp = False
    
def update(pygame, display, deltatime, cs):
    # tick #
    global hdisp
    global sdisp
    pressed = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events: 
        if event.type == 256:
            print('Exiting...')
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                hdisp = True
                sdisp = False
            elif event.key == pygame.K_n:
                hdisp = False 
                sdisp = False
            elif event.key == pygame.K_m:
                hdisp = False
                sdisp = True 

    pos = pygame.mouse.get_pos()
    llpos = ((get_lat(pos[0]), get_lon(pos[1])))

    if pygame.mouse.get_pressed() == (1, 0, 0):
        global LAND_LAT
        global LAND_LON
        LAND_LAT = llpos[0]
        LAND_LON = llpos[1]

    if pygame.mouse.get_pressed() == (0, 0, 1):
        global DEST_LAT
        global DEST_LON
        DEST_LAT = llpos[0]
        DEST_LON = llpos[1]

    # render #
    display.fill((0, 255, 0))
    display.blit(MOON_IMG, (0, 0))
    if hdisp:
        display.blit(H_IMG, (0, 0))
    if sdisp:
        display.blit(S_IMG, (0, 0))

    pygame.mouse.set_visible(False)
    pygame.draw.line(display, (0, 0, 0), (pos[0], -1), (pos[0], 501), 2)
    pygame.draw.line(display, (0, 0, 0), (-1, pos[1]), (501, pos[1]), 2)

    pygame.draw.line(display, (255, 0, 0), (get_x(LAND_LAT), get_y(LAND_LON)), (get_x(DEST_LAT), get_y(DEST_LON)), 4)

    # Now plot the two points #
    plot_point_img(display, get_x(LAND_LAT), get_y(LAND_LON), 2)
    plot_point_img(display, get_x(DEST_LAT)+10, get_y(DEST_LON)-16, 1)

    # state #
    return cs

