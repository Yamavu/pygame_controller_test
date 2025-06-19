from typing import Optional, Mapping, Tuple
from argparse import ArgumentParser

import pygame

from part.pad import XBox_Pad, SNES_Pad

def joystick_init(joystick:Optional[pygame.joystick.Joystick]) -> Optional[pygame.joystick.Joystick]:
    try:
        joystick = pygame.joystick.Joystick(-1)
        if not joystick.get_init():
            joystick.init()
        return joystick
    except pygame.error:
        return None



def main(window=False):
    window = args.window
    unscaled = args.unscaled
    pygame.init()
    screen_width, screen_height = 640, 480
    flags = 0
    if not window and not unscaled:
        flags = pygame.SCALED | pygame.FULLSCREEN
    if not unscaled:
        flags = pygame.SCALED
    if not window:
        flags = pygame.FULLSCREEN
    screen = pygame.display.set_mode((screen_width, screen_height), flags=flags)
    pygame.display.set_caption("Controller Test")
    clock = pygame.time.Clock()
    # define joypad event vars
    joypad_size = None
    joypad = None
    scale = 1
    output_surface:pygame.Surface = None
    output_rect:pygame.Rect = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.JOYDEVICEADDED:
                # init joypad
                #joypad = XBox_Pad(pygame.joystick.Joystick(event.device_index))
                joypad = SNES_Pad(pygame.joystick.Joystick(event.device_index))
                joypad.draw()
                joypad_size = joypad.get_rect()
                scale = min(
                    int(screen_width/joypad_size.width),
                    int(screen_height/joypad_size.height)
                )
                output_surface:pygame.Surface = pygame.Surface(
                    (joypad_size.width*scale, joypad_size.height*scale)
                )
                output_rect:pygame.Rect = output_surface.get_rect(
                    center=(screen.get_width() // 2,screen.get_height() // 2)
                )
                print(f"Joypad {event.device_index} added")
            if event.type == pygame.JOYDEVICEREMOVED and joypad.instance_id == event.device_index:
                joypad = None
                print(f"Joypad {event.device_index} removed")
            if joypad is None:
                continue
            else:
                joypad.update(event)
        screen.fill((0, 0, 0))
        if joypad is None:
            font = pygame.font.Font(None, 32)
            text = font.render("no controller detected", True, (140, 120, 120))
            textpos = text.get_rect(
                center=(screen.get_width() / 2,screen.get_height() / 2)
            )
            screen.blit(text,textpos)
        else:
            pygame.transform.scale_by(joypad,(scale,scale),output_surface)
            screen.blit(output_surface, output_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--window', action='store_true')
    parser.add_argument('--unscaled', action='store_true')
    args = parser.parse_args()
    main(args)
