import sys
import Utils as u

textboxes = []


def init(pg):
    global textboxes
    textboxes.append(u.Textbox(pg, 140, 10, 0, 0, 'Go2DaMoon', (255, 255, 255), 54))
    textboxes.append(u.Textbox(pg, 100, 100, 0, 0, 'Land Lat', (255, 255, 255), 36))
    textboxes.append(u.Textbox(pg, 300, 100, 0, 0, 'Land Lon', (255, 255, 255), 36))
    textboxes.append(u.Textbox(pg, 100, 200, 0, 0, 'Dest Lat', (255, 255, 255), 36))
    textboxes.append(u.Textbox(pg, 300, 200, 0, 0, 'Dest Lon', (255, 255, 255), 36))


def update(pygame, display, deltatime, cs):
    # tick #
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
            if event.type == 256:
                print('Exiting...')
                pygame.quit()
                sys.exit()

    # render #
    display.fill((19, 27, 35))

    for tb in textboxes:
        tb.render(pygame, display)

    # state #
    return cs

