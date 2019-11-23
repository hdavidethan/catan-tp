import pygame, copy
from pygame import gfxdraw
from pygameFramework import PygameGame
from resources.gui.button import Button
from resources.game.board import Board
from config.colors import Colors
from config.config import windowConfig
from config.text import Text
from resources.game.math import CatanMath

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
        menuButton1 = Button(windowConfig.MENU_B1,windowConfig.MENU_B1_SIZE, 'Start Game', menuButtonColors, ('changeMode', 'game'), 0.4)
        menuButton2 = Button(windowConfig.MENU_B2, windowConfig.MENU_B2_SIZE, 'Quit Game', menuButtonColors, ('quit', None), 0.4)
        self.elements.add(menuButton1)
        self.elements.add(menuButton2)
    
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
            self.drawGame(screen)

    def drawGame(self, screen):
        # self.drawGUI(screen)
        self.drawBoard(screen)

    def drawMenu(self, screen):
        for element in self.elements:
            element.draw(screen)

    def inBounds(self, pos, bounds):
        x, y = pos
        x0, y0, x1, y1 = bounds
        return (x > x0 and x < x1 and y > y0 and y < y1)
    
    # Draws the Catan Board
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
                tile = self.board.hexBoard[i][j+firstIndex]
                hexFill = self.getFill(tile)
                leftOffset = ((self.board.q - rowLen) / 2) * hexWidth + boardBounds[0]
                x0 = leftOffset + j * hexWidth
                x1 = leftOffset + (j + 1) * hexWidth
                y0 = i * ySpacing + boardBounds[1]
                y1 = y0 + hexHeight
                center = (int(x0 + (x1-x0)/2), int(y0 + (y1-y0)/2))
                hexPoints = CatanMath.getHexagonPoints((x0, y0, x1, y1))
                pygame.draw.polygon(screen, hexFill, hexPoints)
                self.drawPorts(screen, (i, j+firstIndex), hexPoints, center)
                gfxdraw.aapolygon(screen, hexPoints, Colors.BLACK)
                self.drawTokens(screen, hexHeight, (i, j+firstIndex), center)
                self.drawRoads(screen, tile, hexPoints)
                self.drawNodes(screen, hexHeight, tile, hexPoints)

    def drawRoads(self, screen, tile, hexPoints):
        edgeIndex = 0
        for edge in tile.edges:
            if (edge.road != None):
                point1 = hexPoints[edgeIndex]
                point2 = hexPoints[(edgeIndex+1)%6]
                roadOwner = edge.road
                roadArgs = CatanMath.getThickAALine(point1, point2)
                gfxdraw.filled_polygon(screen, roadArgs, Colors.BLACK)
                gfxdraw.aapolygon(screen, roadArgs, Colors.BLACK)
            edgeIndex += 1

    def drawNodes(self, screen, hexHeight, tile, hexPoints):
        nodeIndex = 0
        nodeSize = int(0.1 * hexHeight)
        for node in tile.nodes:
            if (node.nodeLevel != None):
                number = node.nodeLevel
                center = hexPoints[nodeIndex]
                cx, cy = center
                cx, cy = int(cx), int(cy)
                pygame.draw.circle(screen, Colors.WHITE, (cx, cy), nodeSize)
                gfxdraw.aacircle(screen, cx, cy, nodeSize, Colors.BLACK)
                nodeText = Text.NODE_FONT.render(str(number), True, Colors.BLACK)
                nodeSurf = nodeText.get_rect()
                nodeSurf.center = (cx, cy)
                screen.blit(nodeText, nodeSurf)
            nodeIndex += 1


    def drawTokens(self, screen, hexHeight, pos, center):
        i, j = pos
        tokenSize = int(0.17 * hexHeight)
        number = self.board.hexBoard[i][j].number
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
    
    def drawPorts(self, screen, currentPos, hexPoints, center):
        portLocations = [[(0,3), (0,1)], [(0,4), (1,2)], [(1,1), (0,1)],
                        [(1,4), (2,3)], [(2,0), (0, 5)], [(3,0), (4,5)],
                        [(3,3), (2,3)], [(4,1), (4,5)], [(4,2), (3,4)]]
        portIndex = 0
        for port in portLocations:
            if (currentPos == port[0]):
                pos, nodes = port
                point1 = hexPoints[nodes[0]]
                point2 = hexPoints[nodes[1]]
                triangle = CatanMath.getEqTriangle(screen, point1, point2, center)
                gfxdraw.aapolygon(screen, triangle, Colors.GOLD_1)
                cx, cy = triangle[2]
                cx, cy = int(cx), int(cy)
                portSize = int(0.2 * self.boardSize / 4)
                pygame.draw.circle(screen, Colors.WHITE, (cx, cy), portSize)
                gfxdraw.aacircle(screen, cx, cy, portSize, Colors.BLACK)
                portText = self.getPortText(portIndex)
                portLabel = Text.PORT_FONT.render(portText, True, Colors.BLACK)
                portSurf = portLabel.get_rect()
                portSurf.center = (cx, cy)
                screen.blit(portLabel, portSurf)
            portIndex += 1
    
    def getPortText(self, portIndex):
        port = self.board.ports[portIndex]
        ports = {'wildcard':'? 3:1', 'lumber':'L 2:1', 'sheep':'S 2:1',
                'grain':'G 2:1', 'brick':'B 2:1', 'ore':'O 2:1'}
        return ports[port]
    
    def getFill(self, tile):
        colors = {'forest':Colors.FOREST, 'desert':Colors.DESERT,
                  'hills':Colors.HILLS, 'mountains':Colors.MOUNTAINS,
                  'pasture':Colors.PASTURE, 'fields':Colors.FIELDS,
                  None:Colors.WHITE}
        tileFill = colors[tile.type]
        return tileFill

CatanGame(width=windowConfig.WIDTH, height=windowConfig.HEIGHT, title='Catan: The Settlers of Python').run()