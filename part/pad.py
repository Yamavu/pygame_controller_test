
from typing import Mapping, Tuple

import pygame
from pygame.math import Vector2

from .analogue_stick import AnalogueStick
from .d_pad import D_Pad
from .button import Button, Button1, Button2, Button3
from .analogue_trigger import AnalogueTrigger
from .colors import BUTTON, PAD


class Pad(pygame.Surface):
    def __init__(self, size:Vector2, instance:pygame.joystick.JoystickType):
        super().__init__(size.xy)
        self.instance = instance
        self._pad_c = Vector2(150, 70)
        self.hats: Mapping[int, D_Pad] = {}
        self.buttons: Mapping[int, Button] = {}
        self.sticks: Mapping[Tuple[int, int], AnalogueStick] = {}
        self.triggers: Mapping[int, AnalogueTrigger] = {}

    def _update_axis(self,event) -> bool:
        change_detected = False
        for axes in self.sticks:
            if event.axis == axes[0]:
                self.sticks[axes].setX(event.value)
                change_detected = True
            if event.axis == axes[1]:
                self.sticks[axes].setY(event.value)
                change_detected = True
        for axis in self.triggers:
            if event.axis == axis:
                self.triggers[axis].set_pressure(event.value)
                change_detected = True
        print(
            f"{event.axis}/{self.instance.get_numaxes()}" +
            f": {event.value=}")
        return change_detected

    def update(self, event) -> None:
        if event is None:
            return
        change_detected = False
        if event.type == pygame.JOYAXISMOTION:
            _change_detected = self._update_axis(event)
            change_detected = change_detected or _change_detected
        elif event.type == pygame.JOYHATMOTION:
            if event.hat == 0:
                direction = event.value
                self.hats[0].direction = direction
                change_detected = True
            print(f"{event.hat=}: {event.value=}")
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button in self.buttons:
                self.buttons[event.button].active = True
                change_detected = True
            print(f"button #{event.button} pressed")
        elif event.type == pygame.JOYBUTTONUP:
            if event.button in self.buttons:
                self.buttons[event.button].active = False
                change_detected = True
            print(f"button #{event.button} released")
        if change_detected:
            self.draw()

    def draw(self):
        for hat in self.hats.values():
            hat.draw(self)
        for stick in self.sticks.values():
            stick.draw(self)
        for button in self.buttons.values():
            if button in self.sticks.values():
                continue
            button.draw(self)
        for trigger in self.triggers.values():
            trigger.draw(self)


class SNES_Pad(Pad):
    def __init__(self, instance: pygame.joystick.JoystickType):
        super().__init__(Vector2(300, 120), instance)
        pad_c = self._pad_c
        button_c = pad_c + (100, 0)
        self.hats: Mapping[int, D_Pad] = {
            0: D_Pad(0, pad_c+(-100, 0))
        }
        self.buttons: Mapping[int, Button] = {
            0: Button1("B", button_c + (0, 25)),
            1: Button1("A", button_c + (25, 0)),
            2: Button1("Y", button_c + (-25, 0)),
            3: Button1("X", button_c + (0, -25)),
            4: Button3("L", pad_c + (-130, -55), None),
            5: Button3("R", pad_c + (130, -55), None),
            6: Button2("-Select", pad_c + (-25, 0)),
            7: Button2("+Start", pad_c + (25, 0)),
        }
        self.sticks: Mapping[Tuple[int, int], AnalogueStick] = {}
        self.triggers: Mapping[int, AnalogueTrigger] = {}

    def draw(self):
        self.fill(PAD)
        pygame.draw.rect(
            self,
            color=BUTTON,
            rect=self.get_bounding_rect(),
            width=4)
        super().draw()


class XBox_Pad(Pad):
    def __init__(self, instance: pygame.joystick.JoystickType):
        super().__init__(Vector2(300, 120), instance)
        pad_c = self._pad_c
        button_c = pad_c + (100, 0)
        self.hats: Mapping[int, D_Pad] = {
            0: D_Pad(0, pad_c+(-100, 0))
        }
        self.sticks: Mapping[Tuple[int, int], AnalogueStick] = {
            (0, 1): AnalogueStick("L", pad_c+(-30, 25)),
            (3, 4): AnalogueStick("R", pad_c+(30, 25))
        }
        self.buttons: Mapping[int, Button] = {
            0: Button1("B", button_c + (0, 25)),
            1: Button1("A", button_c + (25, 0)),
            2: Button1("Y", button_c + (-25, 0)),
            3: Button1("X", button_c + (0, -25)),
            4: Button3("L1", pad_c+(-125, -55), "L"),
            5: Button3("R1", pad_c+(125, -55), "R"),
            6: Button2("-Select", pad_c+(-25, -15)),
            7: Button2("+Start", pad_c+(25, -15)),
            8: self.sticks[(0, 1)],
            9: self.sticks[(3, 4)]
        }
        trigger_range = (-1, 0.999969482421875)
        self.triggers: Mapping[int, AnalogueTrigger] = {
            2: AnalogueTrigger(
                "L2",
                pad_c+(-85, -55),
                analogue_range=trigger_range),
            5: AnalogueTrigger(
                "R2",
                pad_c+(85, -55),
                analogue_range=trigger_range)
        }

    def draw(self):
        self.fill(PAD)
        pygame.draw.rect(
            self,
            color=BUTTON,
            rect=self.get_bounding_rect(),
            width=4)
        super().draw()
