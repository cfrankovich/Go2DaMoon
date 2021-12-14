import sys

ASSETS = []

def loadasset(name, pg):
    asset = pg.image.load(f'{sys.path[0]}/../assets/{name}.png').convert()
    asset.set_colorkey((255, 0, 255))
    return asset

def initassets(pg):
    global ASSETS
    ASSETS.append(loadasset('start', pg)) # 0
    ASSETS.append(loadasset('flag', pg))
    ASSETS.append(loadasset('star', pg)) # 2

class Textbox:
    def __init__(self, pg, x, y, w, h, text, color, fontsize):
        self.text = text
        self.hitbox = pg.Rect(x, y, w, h)
        self.color = color
        self.font = pg.font.Font(None, fontsize)
        self.active = False

    def render(self, pygame, display):
        sur = self.font.render(self.text, True, self.color)
        display.blit(sur, self.hitbox)

    def istouching(self, hitbox2):
        return hitbox2.colliderect(self.hitbox)

    def turnon(self):
        self.active = True

    def turnoff(self):
        self.active = False

