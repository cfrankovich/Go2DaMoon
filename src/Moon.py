import sys
import Utils as u

LAND_LAT = 0.0 
LAND_LON = 0.0 
DEST_LAT = 0.0 
DEST_LON = 0.0 
SCREEN_X = 0
SCREEN_Y = 0

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

