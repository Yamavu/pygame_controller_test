from typing import Literal
import pygame

LR = Literal["L", "R", None]

class AnalogueTrigger():
    def __init__(self, label, center, parent, side=None, radius = 15.0, analogue_range=(-1,1)):
        self.label = label
        self.center = center
        self.parent = parent
        self.size = pygame.math.Vector2(radius*2,radius)
        self.pressure:float = 0 # range 0 - 1
        self.analogue_range = analogue_range
        self.unit = float(self.analogue_range[1]-self.analogue_range[0])/2
        assert self.analogue_range[1] > self.analogue_range[0], "range max should be bigger than range min"
    def set_pressure(self, x:float):
        self.pressure = round((x+self.unit)/(2*self.unit), ndigits=3)
    def draw(self, surface):
        button_col, label_col, active_col = self.parent.button_cols
        #x,y = self.pos
        btn_rect = pygame.Rect((0,0),self.size)
        btn_rect.center = self.center
        font = pygame.font.Font(None, 16)
        text = font.render(self.label, True, label_col)
        textpos = text.get_rect(center=btn_rect.center)        
        pygame.draw.rect(surface, button_col, btn_rect)
        if self.pressure > 0.001:
            active_rect = btn_rect
            active_rect.right = active_rect.left + self.size.x * self.pressure
            print(f"{self.label} {self.pressure=}")
            pygame.draw.rect(surface, active_col, active_rect)
        surface.blit(text,textpos)