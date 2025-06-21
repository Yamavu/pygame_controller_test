from typing import Literal
import pygame

from .colors import ACTIVE, BUTTON, PAD as LABEL

LR = Literal["L", "R", None]


class AnalogueTrigger():
    def __init__(
            self,
            label,
            center,
            side=None,
            radius=15.0,
            analogue_range=(-1, 1)):
        self.label = label
        self.center = center
        self.size = pygame.math.Vector2(radius*2, radius)
        self.pressure: float = 0  # range 0 - 1
        self.analogue_range = analogue_range
        self.unit = float(self.analogue_range[1]-self.analogue_range[0])/2
        assert self.analogue_range[1] > self.analogue_range[0], \
            "range max should be bigger than range min"

    def set_pressure(self, x: float):
        self.pressure = round((x+self.unit)/(2*self.unit), ndigits=3)
    
    def draw(self, surface):
        btn_rect = pygame.Rect((0, 0), self.size)
        btn_rect.center = self.center
        font = pygame.font.Font(None, 16)
        text = font.render(self.label, True, LABEL)
        textpos = text.get_rect(center=btn_rect.center)        
        pygame.draw.rect(surface, BUTTON, btn_rect)
        if self.pressure > 0.001:
            active_rect = btn_rect
            active_rect.right = active_rect.left + self.size.x * self.pressure
            print(f"{self.label} {self.pressure=}")
            pygame.draw.rect(surface, ACTIVE, active_rect)
        surface.blit(text, textpos)
