from element import Element
from resources.roundedRect import drawRoundedRect
from config.colors import Colors
import pygame

class Button(Element):
    def __init__(self, pos, size, text, color, radius=0):
        super().__init__(pos, size)
        self.radius = radius
        self.color = color
    
    def draw(self, screen):
        rectArgs = (self.pos[0], self.pos[1], self.size[0], self.size[1])
        if (self.radius == 0):
            pygame.draw.rect(screen, self.color, rectArgs)
        else:
            drawRoundedRect(screen, rectArgs, self.color, self.radius)