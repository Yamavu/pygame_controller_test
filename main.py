from typing import Optional, Mapping, Tuple

import pygame

from part.pad import Pad

def joystick_init(joystick:Optional[pygame.joystick.Joystick]) -> Optional[pygame.joystick.Joystick]:
    try:
        joystick = pygame.joystick.Joystick(-1)
        if not joystick.get_init():
            joystick.init()
        return joystick
    except pygame.error:
        return None


def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Controller Test")
    clock = pygame.time.Clock()
    pygame.joystick.init()
    j = Pad()
    j.update()
    joystick:Optional[pygame.joystick.Joystick] = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
            if event.type == pygame.JOYDEVICEREMOVED and joystick.get_instance_id == event.device_index:
                joystick = None
            if not joystick:
                continue
            if event.type == pygame.JOYAXISMOTION:
                for axes in j.sticks:
                    if event.axis == axes[0]:
                        j.sticks[axes].setX(event.value)
                        j.update()
                    if event.axis == axes[1]:
                        j.sticks[axes].setY(event.value)
                        j.update()
                for axis in j.triggers:
                    if event.axis == axis:
                        j.triggers[axis].set_pressure(event.value)
                        j.update()
                print(f"{event.axis}/{joystick.get_numaxes()}: {event.value=}")
            elif event.type == pygame.JOYHATMOTION:
                if event.hat == 0:
                    direction = event.value
                    j.hats[0].direction = direction
                    j.update()
                #if direction != (0,0):
                print(f"{event.hat=}: {event.value=}")
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in j.buttons:
                    #j.buttons[event.button].pressed()
                    j.buttons[event.button].active = True
                    j.update()
                print(f"button #{event.button} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                if event.button in j.buttons:
                    j.buttons[event.button].active = False
                    j.update()
                print(f"button #{event.button} released")
        screen.fill((0, 0, 0))
        if joystick is None:
            font = pygame.font.Font(None, 32)
            text = font.render("no controller detected", True, (140, 120, 120))
            textpos = text.get_rect(
                center=(screen.get_width() / 2,screen.get_height() / 2)
            )
            screen.blit(text,textpos)
        else:
            c = pygame.transform.scale2x(j)
            c_pos = c.get_rect(
                center=(screen.get_width() // 2,screen.get_height() // 2)
            )
            screen.blit(c, c_pos)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
