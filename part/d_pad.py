import pygame

from .colors import ACTIVE, BUTTON, PAD as LABEL


class D_Pad():
    def __init__(self, id, center):
        self.id = id
        self.center = center
        self.radius = 15.0
        self.direction = 0, 0
    
    def draw(self, surface):
        x, y = self.center
        r = 0.8*self.radius
        _r = (2/3)*r
        
        def _arr(direction) -> pygame.Surface:
            dir_btn = pygame.Surface((2*r, 2*r))
            if direction[0] != 0 and self.direction[0] == direction[0]:
                dir_btn.fill(ACTIVE)
            elif direction[1] != 0 and self.direction[1] == direction[1]:
                dir_btn.fill(ACTIVE)
            else:
                dir_btn.fill(BUTTON)
            pygame.draw.polygon(dir_btn, LABEL, points=(
                (_r, 2*_r),
                (2*_r, 2*_r),
                (r, _r/2)))
            if direction == (-1, 0):
                dir_btn = pygame.transform.rotate(dir_btn, angle=90)
            elif direction == (1, 0):
                dir_btn = pygame.transform.rotate(dir_btn, angle=90)
                dir_btn = pygame.transform.flip(
                    dir_btn,
                    flip_y=False,
                    flip_x=True)
            elif direction == (0, -1):
                dir_btn = pygame.transform.flip(
                    dir_btn,
                    flip_y=True,
                    flip_x=False)
            return dir_btn
        
        surface.blit(_arr((1, 0)), dest=(x+25-r, y-r))
        surface.blit(_arr((-1, 0)), dest=(x-25-r, y-r))
        surface.blit(_arr((0, 1)), dest=(x-r, y-25-r))
        surface.blit(_arr((0, -1)), dest=(x-r, y+25-r))
        pygame.draw.circle(
            surface,
            color=BUTTON,
            center=self.center,
            radius=_r)