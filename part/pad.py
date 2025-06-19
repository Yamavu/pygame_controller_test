import pygame

from .analogue_stick import AnalogueStick
from .d_pad import D_Pad
from .button import *
from .analogue_trigger import AnalogueTrigger

class Pad(pygame.Surface):
    
    def update(self, event) -> None:
        if event is None:
            return False
        change_detected = False
        if event.type == pygame.JOYAXISMOTION:
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
            print(f"{event.axis}/{self.instance.get_numaxes()}: {event.value=}")
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
    def __init__(self, instance:pygame.Joystick):
        super().__init__((300,120))
        self.instance = instance
        self.button_cols = ((120,120,120), (64,64,64), (235,64,64))
        pad_c = pygame.math.Vector2(150,70)
        button_c = pad_c + (100,0)
        self.hats:Mapping[int,D_Pad] = {
            0: D_Pad(0,pad_c+(-100,0), self.button_cols)
        }
        self.buttons:Mapping[int, Button] = {
            0 : Button1("B", button_c + (0,25), self),
            1 : Button1("A", button_c + (25,0), self),
            2 : Button1("Y", button_c + (-25,0), self),
            3 : Button1("X", button_c + (0,-25), self),
            4 : Button3("L", pad_c+(-130,-55), self, None),
            5 : Button3("R", pad_c+( 130,-55), self, None),
            6 : Button2("-Select", pad_c+(-25, 0), self),
            7 : Button2("+Start", pad_c+(25, 0), self),
        }
        self.sticks:Mapping[Tuple[int,int],AnalogueStick] = {}
        self.triggers:Mapping[int,AnalogueTrigger] = {}
    def draw(self):
        button_col, label_col, _ = self.button_cols
        self.fill(label_col)
        pygame.draw.rect(self, color=button_col, rect=self.get_bounding_rect(), width=4)
        super().draw()


class XBox_Pad(Pad):
    def __init__(self, instance:pygame.Joystick):
        super().__init__((300,120))
        self.instance = instance
        self.button_cols = ((128,128,128), (64,64,64), (255,64,64))
        pad_c = pygame.math.Vector2(150,70)
        button_c = pad_c + (100,0)
        self.hats:Mapping[int,D_Pad] = {
            0: D_Pad(0,pad_c+(-100,0), self.button_cols)
        }
        self.sticks:Mapping[Tuple[int,int],AnalogueStick] = {
            (0,1): AnalogueStick("L", pad_c+(-30,25), self.button_cols),
            (3,4): AnalogueStick("R", pad_c+(30,25), self.button_cols)
        }
        self.buttons:Mapping[int, Button] = {
            0 : Button1("B", button_c + (0,25), self),
            1 : Button1("A", button_c + (25,0), self),
            2 : Button1("Y", button_c + (-25,0), self),
            3 : Button1("X", button_c + (0,-25), self),
            4 : Button3("L1", pad_c+(-125,-55), self, "L"),
            5 : Button3("R1", pad_c+( 125,-55), self, "R"),
            6 : Button2("-Select", pad_c+(-25, -15), self),
            7 : Button2("+Start", pad_c+(25, -15), self),
            8: self.sticks[(0,1)],
            9: self.sticks[(3,4)]
        }
        trigger_range = (-1, 0.999969482421875)
        self.triggers:Mapping[int,AnalogueTrigger] = {
            2: AnalogueTrigger("L2", pad_c+(-85,-55), self, analogue_range=trigger_range),
            5: AnalogueTrigger("R2", pad_c+( 85,-55), self, analogue_range=trigger_range)
        }
    def draw(self):
        button_col, label_col, _ = self.button_cols
        self.fill(label_col)
        pygame.draw.rect(self, color=button_col, rect=self.get_bounding_rect(), width=4)
        super().draw()