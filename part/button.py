from abc import ABC, abstractmethod
from typing import Literal
import pygame

LR = Literal["L", "R", None]

class Button(ABC):
    def __init__(self, label, center, button_cols, radius = 15.0):
        self.label = label
        self.center = center
        self.button_cols = button_cols
        self.radius = radius
        self.active = False
    @abstractmethod
    def draw(self,surface:pygame.Surface):
        ...
    def pressed(self):
        self.active = True
    def released(self):
        self.active = False

class Button1(Button):
    # Basic Round Button
    def draw(self,surface:pygame.Surface):
        button_col, label_col, active_col = self.button_cols
        r = self.radius
        _col = active_col if self.active else button_col
        pygame.draw.circle(surface=surface,color=_col, center=self.center,radius=r)
        font = pygame.font.Font(None, int(2*r))
        text = font.render(self.label, True, label_col)
        textpos = text.get_rect(center=self.center).move(0,1)
        surface.blit(text,textpos)
    
class Button2(Button):
    # Secondary buttons for Start and Select
    def draw(self, surface):
        long_btn = pygame.Rect((0,0), (self.radius * 2, 2*self.radius //3 ))
        long_btn.center = self.center
        button_col, label_col, active_col = self.button_cols
        font = pygame.font.Font(None, 16)
        text = font.render(self.label, True, button_col)
        textpos = text.get_rect(center=long_btn.center).move(0,16)
        surface.blit(text,textpos)
        _col = active_col if self.active else button_col
        pygame.draw.rect(surface,color=_col, rect=long_btn, border_radius=int(self.radius/3))

class Button3(Button):
    # teriary buttons for bumpers like L or R
    def __init__(self, label, center, button_cols, side:LR = None, radius = 15.0):
        super().__init__(label, center, button_cols, radius)
        self.side = side
    def draw(self, surface):
        size = pygame.math.Vector2(self.radius*2,self.radius)
        button_col, label_col, active_col = self.button_cols
        btn_rect = pygame.Rect((0,0),size)
        btn_rect.center = self.center
        font = pygame.font.Font(None, 16)
        text = font.render(self.label, True, label_col)
        textpos = text.get_rect(center=btn_rect.center)
        _col = active_col if self.active else button_col
        _radius_left = int(self.radius // 3) if self.side == "L" else 0
        _radius_right = int(self.radius // 3) if self.side == "R" else 0
        pygame.draw.rect(surface, _col, btn_rect,border_top_left_radius=_radius_left, border_top_right_radius=_radius_right)
        surface.blit(text,textpos)