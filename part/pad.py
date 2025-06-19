import pygame

from .analogue_stick import AnalogueStick
from .d_pad import D_Pad
from .button import *
from .analogue_trigger import AnalogueTrigger

class Pad(pygame.Surface):
    def __init__(self):
        super().__init__((300,120))
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
            0 : Button1("B", button_c + (0,25), self.button_cols),
            1 : Button1("A", button_c + (25,0), self.button_cols),
            2 : Button1("Y", button_c + (-25,0), self.button_cols),
            3 : Button1("X", button_c + (0,-25), self.button_cols),
            4 : Button3("L1", pad_c+(-125,-55), self.button_cols, "L"),
            5 : Button3("R1", pad_c+( 125,-55), self.button_cols, "R"),
            6 : Button2("-Select", pad_c+(-25, -15), self.button_cols),
            7 : Button2("+Start", pad_c+(25, -15), self.button_cols),
            8: self.sticks[(0,1)],
            9: self.sticks[(3,4)]
        }
        trigger_range = (-1, 0.999969482421875)
        self.triggers:Mapping[int,AnalogueTrigger] = {
            2: AnalogueTrigger("L2", pad_c+(-85,-55), self.button_cols, analogue_range=trigger_range),
            5: AnalogueTrigger("R2", pad_c+( 85,-55), self.button_cols, analogue_range=trigger_range)
        }
        #_buttons = ["B", "A", "Y", "X", "L", "R", "Select", "Start"]
        #self.buttons = {idx:label for idx,label in enumerate(_buttons) if label is not None}
        #_hats = { (0,1,0):"RIGHT", (0,-1,0):"LEFT", (0,0,1):"UP", (0,0,-1):"DOWN" }
    def update(self):
        button_col, label_col, _ = self.button_cols
        self.fill(label_col)
        pygame.draw.rect(self, color=button_col, rect=self.get_bounding_rect(), width=4)
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
        #start = pygame.Rect(110, 50, 30, 10)
        #pygame.draw.rect(self,color=button_col, rect=start,border_radius=2)
        #select = start.move(50,0)
        #pygame.draw.rect(self,color=button_col, rect=select,border_radius=2)