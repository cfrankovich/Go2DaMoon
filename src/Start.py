import sys
import Utils as u

textboxes = []
verbose = False


def data_validation():
    d = float(textboxes[0].text)
    if d < -89.999 or d > -88.0001: 
        print('[0] Out of range.')
        return False

    d = float(textboxes[1].text)
    if d < -179.98109 or d > 179.98109:
        print('[1] Out of range.')
        return False

    d = float(textboxes[2].text)
    if d < -89.999 or d > -88.0001: 
        print('[2] Out of range.')
        return False

    d = float(textboxes[3].text)
    if d < -179.98109 or d > 179.98109:
        print('[3] Out of range.')
        return False

    return True


def init(pg, display, argv):
    global textboxes

    for arg in argv:
        if arg == '-v' or arg == '--verbose':
            global verbose
            verbose = True

    if verbose:
        print('')
        print('[o] Initializing start screen...')
    textboxes.append(u.Textbox(pg, 35, 130, 200, 50, '-89', (0, 0, 0), 40))
    textboxes.append(u.Textbox(pg, 275, 130, 200, 50, '0', (0, 0, 0), 40))

    textboxes.append(u.Textbox(pg, 35, 230, 200, 50, '-88.5', (0, 0, 0), 40))
    textboxes.append(u.Textbox(pg, 275, 230, 200, 50, '40', (0, 0, 0), 40))

    textboxes.append(u.Textbox(pg, 35, 330, 200, 50, '500', (0, 0, 0), 40))
    textboxes.append(u.Textbox(pg, 275, 330, 200, 50, '500', (0, 0, 0), 40))
    if verbose:
        print('[+] Finished initializing start screen')


def update(pygame, display, deltatime, cs):
    # tick #
    pressed = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events: 
            if event.type == 256:
                print('Exiting...')
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if verbose:
                        print('[o] Requesting data submition...')
                    if data_validation():
                        if verbose:
                            print('[+] Data is valid! Placing in temporary location...')
                        f = open('TEMPDATA', 'w')
                        for t in textboxes:
                            f.write(f'{t.text}\n')
                        f.close()
                        if verbose:
                            print('[o] Moving on to image rendering process')
                        return 1
                    else:
                        print('[-] Error with validation (user error)')


    # render #
    display.fill((19, 27, 35))
    display.blit(u.ASSETS[0], (0, 0))

    # yuck #
    for box in textboxes:
        box.render(pygame, display)
        if box.active:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        box.text = box.text[0:-1]
                    else:
                        box.text += event.unicode
        if pygame.mouse.get_pressed() == (1, 0, 0):
            box.turnoff()
            mpos = pygame.mouse.get_pos()
            temp = pygame.Rect(mpos[0], mpos[1], 5, 5)
            if box.istouching(temp):
                box.turnon()

    # state #
    return cs

