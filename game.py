import pygame
from pygameFramework import PygameGame
from resources.roundedRect import drawRoundedRect
from config.colors import *
from config.config import *

# TODO: Make Buttons OOPy
# TODO: Create Board Representation

class CatanGame(PygameGame):
    # Run on app init
    def init(self):
        self._debugMenu = True
        self._debugBoard = not self._debugMenu

    def keyPressed(self, key, mod):
        if (key == pygame.K_m):
            self._debugMenu = not self._debugMenu

    def redrawAll(self, screen):
        if (self._debugMenu):
            self.drawMenu(screen)
        if (self._debugBoard):
            # self.drawGUI(screen)
            self.drawBoard(screen)

    def drawMenu(self, screen):
        self.width, self.height = screen.get_size()
        cx = self.width / 2
        menuPos = (cx, 3/5*self.height)
        mx, my = pygame.mouse.get_pos()
        b1Color = Colors.gold1
        b2Color = Colors.gold2
        b1Width = b2Width = 0.25 * self.width
        b1Height = b2Height = 0.075 * self.height
        b1Pos = (cx, 0.75*menuPos[1])
        b2Pos = (cx, 1.25*menuPos[1])
        # Check if mouse in Button 1
        if (self.inBounds((mx, my), b1Bounds)):
            b1Color = Colors.gold2
        if (self.inBounds((mx, my), b2Bounds)):
            b2Color = Colors.gold2
        drawRoundedRect(screen, b1, b1Color)

    def inBounds(self, pos, bounds):
        x, y = pos
        x0, y0, x1, y1 = bounds
        return (x > x0 and x < x1 and y > y0 and y < y1)
    
    def drawBoard(self, screen):



CatanGame(width=windowConfig.width, height=windowConfig.height, title='The Settlers of Python').run()