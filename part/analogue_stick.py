import pygame

from .button import Button

class AnalogueStick(Button):
    def __init__(self, label, center, button_cols, radius = 15.0):
        self.label = label
        self.center = center
        self.button_cols = button_cols
        self.radius = radius
        self.direction = pygame.math.Vector2(0,0)
        self.active = False
    def pressed(self):
        self.active = True
    def released(self):
        self.active = False
    def setX(self, x:float):
        self.direction[0] = x
    def setY(self, y:float):
        self.direction[1] = y
    def draw(self, surface):
        button_col, label_col, active_col = self.button_cols
        r = self.radius
        x,y = self.center
        pygame.draw.circle(surface, button_col, (x, y), r, width=2)
        pygame.draw.line(surface, button_col, (x-r, y), (x+r, y))
        pygame.draw.line(surface, button_col, (x, y-r), (x, y+r))
        pos = self.direction * r + (x,y)
        if self.active:
            pygame.draw.circle(surface, active_col, pos, radius=10)
        else:
            pygame.draw.circle(surface, button_col, pos, radius=10)
        font = pygame.font.Font(None, 16)
        text = font.render(self.label, True, label_col)
        textpos = text.get_rect(center=pos).move(0,1)
        surface.blit(text,textpos)
        pygame.draw.circle(surface, label_col, pos, radius=10, width=2)
