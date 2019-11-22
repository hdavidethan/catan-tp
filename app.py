import pygame, copy
from pygame import gfxdraw
from pygameFramework import PygameGame
from resources.gui.button import Button
from resources.game.board import Board
from config.colors import Colors
from config.config import windowConfig
from config.text import Text

# TODO: Make Buttons OOPy
# TODO: Create Board Representation

class CatanGame(PygameGame):
    # Run on app init
    def init(self):
        self.boardSize = min(self.width*0.7, self.height*0.7)
        self.board = Board()
        self.elements = set()
        self.activeMode = None
        self.setActiveMode('menu')
    
    def setActiveMode(self, mode):
        if (mode == 'menu'):
            self.initMenu()
            self.activeMode = 'menu'
        elif (mode == 'game'):
            self.initGame()
            self.activeMode = 'game'

    def initMenu(self):
        self.elements = set()
        menuButtonColors = [Colors.GOLD_1, Colors.GOLD_2]
        menuButton1 = Button(windowConfig.MENU_B1, windowConfig.MENU_B1_SIZE, 'Start Game', menuButtonColors, 0.4)
        self.elements.add(menuButton1)
    
    def initGame(self):
        self.elements = set()

    def keyPressed(self, key, mod):
        if (self.activeMode == 'game'):
            if (key == pygame.K_m):
                self.activeMode = 'menu'
            elif (key == pygame.K_r):
                self.board = Board()
        
    def mousePressed(self, mx, my):
        for element in self.elements:
            x0, y0, width, height = element.getRectArgs()
            x1 = x0 + width
            y1 = y0 + height
            if (mx > x0 and mx < x1 and my > y0 and my < y1):
                element.onClick(self)

    def redrawAll(self, screen):
        if (self.activeMode == 'menu'):
            self.drawMenu(screen)

        if (self.activeMode == 'game'):
            # self.drawGUI(screen)
            self.drawBoard(screen)

    def drawMenu(self, screen):
        for element in self.elements:
            element.draw(screen)

    def inBounds(self, pos, bounds):
        x, y = pos
        x0, y0, x1, y1 = bounds
        return (x > x0 and x < x1 and y > y0 and y < y1)
    
    def drawBoard(self, screen):
        cx, cy = self.width/2, self.height/2
        heightToWidthRatio = 32 / 35
        boardBounds = (cx-self.boardSize/2, cy-(self.boardSize/heightToWidthRatio)/2,
                        cx+self.boardSize/2, cy+(self.boardSize/heightToWidthRatio)/2)
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
                leftOffset = ((self.board.q - rowLen) / 2) * hexWidth + boardBounds[0]
                x0 = leftOffset + j * hexWidth
                x1 = leftOffset + (j + 1) * hexWidth
                y0 = i * ySpacing + boardBounds[1]
                y1 = y0 + hexHeight
                pygame.draw.polygon(screen, hexFill, 
                    self.getHexagonPoints((x0, y0, x1, y1)))
                gfxdraw.aapolygon(screen, self.getHexagonPoints((x0, y0, x1, y1)), Colors.BLACK)

                # Draw Token
                center = (int(x0 + (x1-x0)/2), int(y0 + (y1-y0)/2))
                tokenSize = int(0.17 * hexHeight)
                number = self.board.hexBoard[i][j+firstIndex].number
                if (number != None):
                    pygame.draw.circle(screen, Colors.WHITE, center, tokenSize)
                    gfxdraw.aacircle(screen, center[0], center[1], tokenSize, Colors.BLACK)
                    if (number in [6, 8]):
                        tokenColor = Colors.BLACK
                    else:
                        tokenColor = Colors.BLACK
                    token = Text.TOKEN_FONT.render(str(number), True, tokenColor)
                    tokenSurf = token.get_rect()
                    tokenSurf.center = center
                    screen.blit(token, tokenSurf)

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
        colors = {'forest':Colors.FOREST, 'desert':Colors.DESERT,
                  'hills':Colors.HILLS, 'mountains':Colors.MOUNTAINS,
                  'pasture':Colors.PASTURE, 'fields':Colors.FIELDS,
                  None:Colors.WHITE}
        tileFill = colors[tile.type]
        return tileFill

CatanGame(width=windowConfig.WIDTH, height=windowConfig.HEIGHT, title='Catan: The Settlers of Python').run()