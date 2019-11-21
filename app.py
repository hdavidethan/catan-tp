import pygame, copy
from pygame import gfxdraw
from pygameFramework import PygameGame
from resources.gui.roundedRect import drawRoundedRect
from resources.game.board import Board
from config.colors import *
from config.config import *

# TODO: Make Buttons OOPy
# TODO: Create Board Representation

class CatanGame(PygameGame):
    # Run on app init
    def init(self):
        self.boardSize = min(self.width*0.7, self.height*0.7)
        self.board = Board()
        self._debugMenu = False
        self._debugBoard = True

    def keyPressed(self, key, mod):
        if (key == pygame.K_m):
            self._debugMenu = not self._debugMenu
        elif (key == pygame.K_r):
            self.board = Board()

    def redrawAll(self, screen):
        if (self._debugMenu):
            #self.drawMenu(screen)
            pass
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
        cx, cy = self.width/2, self.height/2
        heightToWidthRatio = 32 / 35
        boardBounds = (cx-self.boardSize/2, cy-self.boardSize/heightToWidthRatio,
                        cx+self.boardSize/2, cy+self.boardSize/heightToWidthRatio)
        hexWidth = self.boardSize / 5
        hexHeight = self.boardSize / 4
        ySpacing = hexHeight * 3 / 4
        for i in range(self.board.q):
            row = copy.copy(self.board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = self.board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen):
                hexFill = self.getFill(self.board.hexBoard[i][j+firstIndex])
                leftOffset = ((self.board.q - rowLen) / 2) * hexWidth
                x0 = leftOffset + j * hexWidth
                x1 = leftOffset + (j + 1) * hexWidth
                y0 = i * ySpacing
                y1 = y0 + hexHeight
                pygame.draw.polygon(screen, hexFill, 
                    self.getHexagonPoints((x0, y0, x1, y1)))
                gfxdraw.aapolygon(screen, self.getHexagonPoints((x0, y0, x1, y1)), Colors.black)

    def getHexagonPoints(self, bounds):
        x0, y0, x1, y1 = bounds
        width = x1 - x0
        height = y1 - y0
        point1 = (x0, y0 + height/4)
        point2 = (x0+width/2, y0)
        point3 = (x1, y0 + height/4)
        point4 = (x1, y0 + 3*height/4)
        point5 = (x0+width/2, y1)
        point6 = (x0, y0 + 3*height/4)
        return [point1, point2, point3, point4, point5, point6]
    
    def getFill(self, tile):
        colors = {'forest':Colors.forest, 'desert':Colors.desert,
                  'hills':Colors.hills, 'mountains':Colors.mountains,
                  'pasture':Colors.pasture, 'fields':Colors.fields,
                  None:Colors.white}
        tileFill = colors[tile.type]
        return tileFill

CatanGame(width=windowConfig.width, height=windowConfig.height, title='Catan: The Settlers of Python').run()