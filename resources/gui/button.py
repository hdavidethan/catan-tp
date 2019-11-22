from resources.gui.element import Element
from resources.gui.roundedRect import drawRoundedRect
from config.colors import Colors
from config.text import Text
import pygame

class Button(Element):
    def __init__(self, pos, size, text, colors, radius=0):
        super().__init__(pos, size)
        self.text = text
        self.radius = radius
        self.colors = colors
    
    def __eq__(self, other):
        return isinstance(other, Button) and (self.pos == other.pos)
    
    def __hash__(self):
        return hash((self.pos, self.size, self.text))

    def getColor(self, rectArgs):
        mx, my = pygame.mouse.get_pos()
        x0, y0, width, height = rectArgs
        x1, y1 = x0 + width, y0 + height
        if (mx > x0 and mx < x1 and my > y0 and my < y1):
            return self.colors[1]
        else:
            return self.colors[0]
    
    def onClick(self, game):
        game.activeMode = 'game'
    
    def draw(self, screen):
        rectArgs = self.getRectArgs()
        setColor = self.getColor(rectArgs)
        if (self.radius == 0):
            pygame.draw.rect(screen, setColor, rectArgs)
        else:
            drawRoundedRect(screen, rectArgs, setColor, self.radius)
        text = Text.BUTTON_FONT.render(self.text, True, Colors.BLACK)
        textSurf = text.get_rect()
        textSurf.center = self.pos
        screen.blit(text, textSurf)