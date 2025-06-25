from typing import Literal, Protocol, Callable, Dict
from enum import Enum, auto
from functools import partial

import pygame
from pygame.math import Vector2
from pygame import Surface

from .colors import ACTIVE, BUTTON, PAD as LABEL


class GenericButton(Protocol):
    def released(self):
        ...

    def pressed(self):
        ...

    def draw(self, surface: Surface):
        ...


class Shape(Enum):
    Round = auto()
    Long = auto()
    Bumper = auto()
    LeftBumper = auto()
    RightBumper = auto()


LR = Literal["L", "R", None]


def draw_round_button(instance: "Button", surface: Surface):
    r = instance.radius
    _col = ACTIVE if instance.active else BUTTON
    pygame.draw.circle(
        surface=surface,
        color=_col,
        center=instance.center,
        radius=r)
    _move = Vector2(0, 1)
    instance._draw_label(
        instance.center,
        surface,
        font_size=int(2*r),
        move=_move)


def draw_secondary_button(instance: "Button", surface):
    long_btn = pygame.Rect(
        (0, 0),
        (instance.radius * 2, 2*instance.radius // 3))
    long_btn.center = instance.center
    _col = ACTIVE if instance.active else BUTTON
    pygame.draw.rect(
        surface,
        color=_col,
        rect=long_btn,
        border_radius=int(instance.radius/3))
    _move = Vector2(0, 16)
    instance._draw_label(long_btn.center, surface, color=BUTTON, move=_move)


def draw_bumper(instance: "Button", surface, side: LR = None):
    size = pygame.math.Vector2(instance.radius*2, instance.radius)
    btn_rect = pygame.Rect((0, 0), size)
    btn_rect.center = instance.center
    _col = ACTIVE if instance.active else BUTTON
    if instance.shape == Shape.LeftBumper:
        _radius_left = int(instance.radius // 3)
    else:
        _radius_left = 0
    if instance.shape == Shape.RightBumper:
        _radius_right = int(instance.radius // 3)
    else:
        _radius_right = 0
    pygame.draw.rect(
        surface,
        _col, btn_rect,
        border_top_left_radius=_radius_left,
        border_top_right_radius=_radius_right)
    instance._draw_label(btn_rect.center, surface)


DRAW_FUNCTIONS: Dict[Shape, Callable[[GenericButton, Surface], None]] = {
    Shape.Round: draw_round_button,
    Shape.Long: draw_secondary_button,
    Shape.Bumper: draw_bumper,
    Shape.LeftBumper: partial(draw_bumper, side="L"),
    Shape.RightBumper: partial(draw_bumper, side="R")
}


class Button:
    def __init__(self, label: str, center, shape: Shape, radius: float = 15.0):
        self.label = label
        self.center = center
        self.shape = shape
        self.radius = radius
        self.active = False
        if self.shape not in DRAW_FUNCTIONS:
            raise NotImplementedError()
        self.draw_function = DRAW_FUNCTIONS[self.shape]

    def draw(self, surface: Surface) -> None:
        self.draw_function(self, surface)

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
