from abc import ABC, abstractmethod
from typing import Literal

import pygame
from pygame.math import Vector2

from .colors import ACTIVE, BUTTON, PAD as LABEL

LR = Literal["L", "R", None]


class Button(ABC):
    def __init__(self, label: str, center, radius=15.0):
        self.label = label
        self.center = center
        self.radius = radius
        self.active = False

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        ...

    def _draw_label(
            self,
            center,
            surface,
            font=None,
            font_size: int = 16,
            color=LABEL,
            move: Vector2 = Vector2(0, 0)):
        font = pygame.font.Font(font, font_size)
        text = font.render(self.label, True, color)
        textpos = text.get_rect(center=center).move(move)
        surface.blit(text, textpos)

    def pressed(self):
        self.active = True

    def released(self):
        self.active = False


class Button1(Button):
    # Basic Round Button
    def draw(self, surface: pygame.Surface):
        r = self.radius
        _col = ACTIVE if self.active else BUTTON
        pygame.draw.circle(
            surface=surface,
            color=_col,
            center=self.center,
            radius=r)
        _move = Vector2(0, 1)
        self._draw_label(self.center, surface, font_size=int(2*r), move=_move)


class Button2(Button):
    # Secondary buttons for Start and Select
    def draw(self, surface):
        long_btn = pygame.Rect((0, 0), (self.radius * 2, 2*self.radius // 3))
        long_btn.center = self.center
        _col = ACTIVE if self.active else BUTTON
        pygame.draw.rect(
            surface,
            color=_col,
            rect=long_btn,
            border_radius=int(self.radius/3))
        _move = Vector2(0, 16)
        self._draw_label(long_btn.center, surface, color=BUTTON, move=_move)


class Button3(Button):
    # teriary buttons for bumpers like L or R
    def __init__(
            self,
            label,
            center,
            side: LR = None,
            radius=15.0):
        super().__init__(label, center, radius)
        self.side = side

    def draw(self, surface):
        size = pygame.math.Vector2(self.radius*2, self.radius)
        btn_rect = pygame.Rect((0, 0), size)
        btn_rect.center = self.center
        _col = ACTIVE if self.active else BUTTON
        _radius_left = int(self.radius // 3) if self.side == "L" else 0
        _radius_right = int(self.radius // 3) if self.side == "R" else 0
        pygame.draw.rect(
            surface,
            _col, btn_rect,
            border_top_left_radius=_radius_left,
            border_top_right_radius=_radius_right)
        self._draw_label(btn_rect.center, surface)
