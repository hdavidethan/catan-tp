#########################################################################
# Dice File
# Contains the Dice subclass of Element; generates the dice rolls
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

import pygame, random
from pygame import gfxdraw
from resources.gui.element import Element
from resources.gui.roundedRect import drawRoundedRect
from config.colors import Colors
from config.text import Text

class Dice(Element):
    def __init__(self, game, pos, size, index):
        self.game = game
        self.pos = pos
        self.size = size
        self.index = index
        self.value = 0
    
    def roll(self):
        self.value = random.randint(1,6)
    
    def draw(self, screen, game):
        rectArgs = self.getRectArgs()
        x, y, width, height = rectArgs
        diceText = str(self.value)
        color = Colors.GOLD_2 if self.index == 0 else Colors.RED_1
        drawRoundedRect(screen, rectArgs, color, 0.2)
        label = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        label.convert_alpha()
        self.getDiceSurface(label, self.value, rectArgs)
        labelPos = label.get_rect()
        labelPos.center = self.pos
        screen.blit(label, labelPos)
    
    def getDiceSurface(self, surface, n, rectArgs):
        if (n > 0):
            x, y, width, height = rectArgs
            dice = {1:[[False]*3, [False, True, False], [False]*3],
                    2:[[True, False, False], [False]*3, [False, False, True]],
                    3:[[True, False, False], [False, True, False], [False, False, True]],
                    4:[[True, False, True], [False]*3, [True, False, True]],
                    5:[[True, False, True], [False, True, False], [True, False, True]],
                    6:[[True, False, True]]*3}
            diceList = dice[n]
            spacing = width / 7
            for i in range(3):
                for j in range(3):
                    x = 2 * i + 1
                    y = 2 * j + 1
                    x0 = int(x * spacing)
                    y0 = int(y * spacing)
                    x1 = int(x0 + spacing)
                    y1 = int(y0 + spacing)
                    r = spacing / 2
                    cx, cy = x0 + r, y0 + r
                    cx, cy = int(cx), int(cy)
                    r = int(r * 1.5)
                    if (diceList[i][j]):
                        gfxdraw.aacircle(surface, cx, cy, r, Colors.WHITE)
                        gfxdraw.filled_circle(surface, cx, cy, r, Colors.WHITE)
                    


        
