import sys

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
        self.color = (0, 255, 0)

    def turnoff(self):
        self.active = False
        self.color = (255, 0, 0)

