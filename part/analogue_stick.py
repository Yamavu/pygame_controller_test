#from math import pow

import pygame
from pygame.math import Vector2

from .button import Button
from .colors import ACTIVE, BUTTON, PAD as LABEL


class AnalogueStick(Button):
    def __init__(self, label:str, center:Vector2, radius=15.0):
        self.label = label
        self.center = center
        self.radius = radius
        self.direction = pygame.math.Vector2(0, 0)
        self.active = False

    def pressed(self):
        self.active = True

    def released(self):
        self.active = False

    def setX(self, x: float):
        self.direction[0] = x

    def setY(self, y: float):
        self.direction[1] = y

    def _map_input(self) -> Vector2:
        v = self.direction.copy()
        if v.x > v.epsilon and v.y > v.epsilon:
            v.scale_to_length((v.x + v.y)/2)
        return v

    def draw(self, surface):
        r = self.radius
        x, y = self.center
        pygame.draw.circle(surface, BUTTON, (x, y), r, width=2)
        pygame.draw.line(surface, BUTTON, (x-r, y), (x+r, y))
        pygame.draw.line(surface, BUTTON, (x, y-r), (x, y+r))
        pos = self._map_input() * r + self.center
        if self.active:
            pygame.draw.circle(surface, ACTIVE, pos, radius=10)
        else:
            pygame.draw.circle(surface, BUTTON, pos, radius=10)
        font = pygame.font.Font(None, 16)
        text = font.render(self.label, True, LABEL)
        textpos = text.get_rect(center=pos).move(0, 1)
        surface.blit(text, textpos)
        pygame.draw.circle(surface, LABEL, pos, radius=10, width=2)
