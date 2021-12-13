import sys
import Utils as u

textboxes = []


def data_validation():
    return True
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


def init(pg):
    global textboxes

    textboxes.append(u.Textbox(pg, 35, 130, 200, 50, '0', (0, 0, 0), 40))
    textboxes.append(u.Textbox(pg, 275, 130, 200, 50, '0', (0, 0, 0), 40))

    textboxes.append(u.Textbox(pg, 35, 230, 200, 50, '0', (0, 0, 0), 40))
    textboxes.append(u.Textbox(pg, 275, 230, 200, 50, '0', (0, 0, 0), 40))

    textboxes.append(u.Textbox(pg, 35, 330, 200, 50, '500', (0, 0, 0), 40))
    textboxes.append(u.Textbox(pg, 275, 330, 200, 50, '500', (0, 0, 0), 40))


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
                    if data_validation():
                        f = open('TEMPDATA', 'w')
                        for t in textboxes:
                            f.write(f'{t.text}\n')
                        f.close()
                        return 1
                    else:
                        print('Error with validation (user error)')


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

