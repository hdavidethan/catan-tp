import pygame, copy, random
from pygame import gfxdraw
from pygameFramework import PygameGame
from resources.gui.button import Button
from resources.game.board import Board
from resources.game.math import CatanMath
from resources.game.player import Player
from resources.gui.scorecard import Scorecard
from resources.gui.dice import Dice
from config.colors import Colors
from config.config import windowConfig
from config.text import Text

class CatanGame(PygameGame):
    # Run on app init
    def init(self):
        self.cx, self.cy = self.width/2, self.height/2
        self.boardSize = min(self.width*0.65, self.height*0.65)
        self.boardBounds = (self.cx-self.boardSize/2, self.cy-(self.boardSize/windowConfig.HEIGHT_TO_WIDTH_RATIO)/2,
                        self.cx+self.boardSize/2, self.cy+(self.boardSize/windowConfig.HEIGHT_TO_WIDTH_RATIO)/2)
        self.hexWidth = self.boardSize / 5
        self.hexHeight = self.boardSize / 4
        self.ySpacing = self.hexHeight * 3 / 4
        self.resetGame()
        self.activeMode = None
        self.setActiveMode('menu')
    
    # Resets all game variables (Board, Player, etc.)
    def resetGame(self):
        self.inBuildMode = False
        self.board = Board()
        self.turn = 0
        self.dice1 = Dice(self, windowConfig.DICE_1, windowConfig.DICE_SIZE, 0)
        self.dice2 = Dice(self, windowConfig.DICE_2, windowConfig.DICE_SIZE, 1)
        self.dice1.roll()
        self.dice2.roll()
        self.currentPlayer = 0

    # Sets the active mode of the app
    def setActiveMode(self, mode):
        if (mode == 'menu'):
            self.initMenu()
            self.activeMode = 'menu'
        elif (mode == 'game'):
            self.initGame()
            self.activeMode = 'game'

    # Runs upon Menu Mode activation/switch
    def initMenu(self):
        self.elements = set()
        menuButton1 = Button(windowConfig.MENU_B1,windowConfig.MENU_B1_SIZE, 'Start Game', Colors.BUTTON_COLORS, ('changeMode', 'game'), 0.4)
        menuButton2 = Button(windowConfig.MENU_B2, windowConfig.MENU_B2_SIZE, 'Quit Game', Colors.BUTTON_COLORS, ('quit', None), 0.4)
        self.elements.add(menuButton1)
        self.elements.add(menuButton2)
    
    # Runs upon Game Mode activation/switch
    def initGame(self):
        self.elements = set()
        self.selectElements = set()
        scores = [windowConfig.SCORE_1, windowConfig.SCORE_2, windowConfig.SCORE_3, windowConfig.SCORE_4]
        scoreCounter = 0
        for player in self.board.players:
            self.elements.add(Scorecard(player, scores[scoreCounter], windowConfig.SCORE_SIZE))
            scoreCounter += 1
        endTurnButton = Button(windowConfig.END_TURN, windowConfig.END_TURN_SIZE, 'End Turn', Colors.BUTTON_COLORS, ('endTurn', None), 0.4)
        self.elements.add(endTurnButton)
        self.elements.add(self.dice1)
        self.elements.add(self.dice2)

        self.buildElements = dict()
        buildRoadButton = Button(windowConfig.BUILD_ROAD, windowConfig.BUILD_ROAD_SIZE, 
                                'Build Road', Colors.BUTTON_COLORS, ('build', 'road'), 0.4, font=Text.BUILD_FONT)
        buildSettleButton = Button(windowConfig.BUILD_SETTLE, windowConfig.BUILD_SETTLE_SIZE,
                                'Build Settlement', Colors.BUTTON_COLORS, ('build', 'settlement'), 0.4, font=Text.BUILD_FONT)
        buildCityButton = Button(windowConfig.BUILD_CITY, windowConfig.BUILD_CITY_SIZE,
                                'Build City', Colors.BUTTON_COLORS, ('build', 'city'), 0.4, font=Text.BUILD_FONT)
        buildDevCardButton = Button(windowConfig.BUILD_DEVCARD, windowConfig.BUILD_DEVCARD_SIZE,
                                'Buy Dev Card', Colors.BUTTON_COLORS, ('build', 'devCard'), 0.4, font=Text.BUILD_FONT)
        self.buildElements['road'] = buildRoadButton
        self.buildElements['settlement'] = buildSettleButton
        self.buildElements['city'] = buildCityButton
        self.buildElements['devCard'] = buildDevCardButton
        self.initRoadsWrapper()
        self.startTurn()
    
    def initRoadsWrapper(self):
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
                leftOffset = ((self.board.q - rowLen) / 2) * self.hexWidth + self.boardBounds[0]
                x0 = leftOffset + j * self.hexWidth
                x1 = leftOffset + (j + 1) * self.hexWidth
                y0 = i * self.ySpacing + self.boardBounds[1]
                y1 = y0 + self.hexHeight
                hexPoints = CatanMath.getHexagonPoints((x0, y0, x1, y1))
                self.initRoads(tile, (x0, y0, x1, y1))
                
    def initRoads(self, tile, tileBounds):
        x0, y0, x1, y1 = tileBounds
        edgeIndex = 0
        hexPoints = CatanMath.getHexagonPoints((x0, y0, x1, y1))
        for edge in tile.edges:
            edgeID = edge.id
            boardEdge = self.board.edges[edgeID]
            if (boardEdge.pos == None):
                point1 = hexPoints[edgeIndex]
                point2 = hexPoints[(edgeIndex+1)%6]
                x1, y1 = point1
                x2, y2 = point2
                center = ((x1 + x2) / 2, (y1 + y2) / 2)
                boardEdge.pos = center
            edgeIndex += 1

    # Handles keystrokes
    def keyPressed(self, key, mod):
        if (self.activeMode == 'game'):
            if (key == pygame.K_m):
                self.setActiveMode('menu')
            elif (key == pygame.K_r):
                self.resetGame()
            elif (key == pygame.K_c):
                for player in self.board.players:
                    player.resources[random.choice(['grain', 'lumber', 'ore', 'sheep', 'brick'])] += 1
    
    def startTurn(self):
        turn = self.currentPlayer
        player = self.board.players[turn]
        self.checkBuildConditions(player)

    def checkBuildConditions(self, player):
        roadCondition = (player.resources['lumber'] >= 1 and player.resources['brick'] >= 1
                            and (len(player.settlements) + len(player.cities)) > 0)
        settlementCondition = (player.resources['lumber'] >= 1 and player.resources['brick'] >= 1
                            and player.resources['grain'] >= 1 and player.resources['sheep'] >= 1)
        cityCondition = (player.resources['ore'] >= 3 and player.resources['grain'] >= 2
                            and len(player.settlements) > 0)
        devCardCondition = (player.resources['sheep'] >= 1 and player.resources['ore'] >= 1 
                            and player.resources['grain'] >= 1)
        conditions = (('road', roadCondition), ('settlement', settlementCondition),
                    ('city', cityCondition), ('devCard', devCardCondition))
        for build in conditions:
            self.buildElements[build[0]].isDisabled = not build[1]
    
    def buildMode(self, build):
        self.inBuildMode = True
        self.selectElements = set()
        if (build == 'settlement'):
            for node in self.board.nodes:
                if (node.nodeLevel == 0 and node.buildable):
                    cx, cy = node.pos
                    nodeButton = Button((cx, cy), windowConfig.BUILD_BUTTON_SIZE,
                            None, Colors.BUTTON_COLORS, ('buildConfirm', (node, self.board.players[self.currentPlayer])), 0.4)
                    self.selectElements.add(nodeButton)
        elif (build == 'city'):
            for node in self.board.nodes:
                if (node.nodeLevel == 1 and node.owner.index == self.currentPlayer):
                    cx, cy = node.pos
                    nodeButton = Button((cx, cy), windowConfig.BUILD_BUTTON_SIZE,
                            None, Colors.BUTTON_COLORS, ('buildConfirm', (node, self.board.players[self.currentPlayer])), 0.4)
                    self.selectElements.add(nodeButton)
        elif (build == 'road'):
            seen = set()
            for node in self.board.nodes:
                if (node.owner != None and node.owner.index == self.currentPlayer):
                    roads = node.getRoads(self.board)
                    for i in roads:
                        seen.add(i)
                else:
                    roads = node.getRoads(self.board)
                    tmp = copy.copy(roads)
                    found = False
                    for i in roads:
                        if (self.board.edges[i].road == self.board.players[self.currentPlayer].bgColor):
                            found = True
                            tmp.remove(i)
                    if (found == True):
                        for i in tmp:
                            seen.add(i)
                for i in seen:
                    edge = self.board.edges[i]
                    if (edge.road == None):
                        cx, cy = edge.pos
                        roadButton = Button((cx, cy), windowConfig.BUILD_BUTTON_SIZE,
                            None, Colors.BUTTON_COLORS, ('buildConfirm', (edge, self.board.players[self.currentPlayer])), 0.4)
                        self.selectElements.add(roadButton)

    # Handles end turn clicks
    def endTurn(self):
        self.turn += 1
        self.currentPlayer = self.turn % 4
        self.dice1.roll()
        self.dice2.roll()
        self.startTurn()
    
    def checkVictoryPoints(self):
        player = self.board.players[self.currentPlayer]
        settlements = len(player.settlements)
        cities = len(player.cities)
        player.victoryPoints = settlements + 2 * cities

    # Handles mouse presses
    def mousePressed(self, mx, my):
        for element in self.elements:
            x0, y0, width, height = element.getRectArgs()
            x1 = x0 + width
            y1 = y0 + height
            if (mx > x0 and mx < x1 and my > y0 and my < y1):
                element.onClick(self)
        if (self.activeMode == 'game'):
            for key in self.buildElements:
                x0, y0, width, height = self.buildElements[key].getRectArgs()
                x1 = x0 + width
                y1 = y0 + height
                if (mx > x0 and mx < x1 and my > y0 and my < y1):
                    self.buildElements[key].onClick(self)
            if (len(self.selectElements) > 0):
                for selectElement in self.selectElements:
                    x0, y0, width, height = selectElement.getRectArgs()
                    x1 = x0 + width
                    y1 = y0 + height
                    if (mx > x0 and mx < x1 and my > y0 and my < y1):
                        selectElement.onClick(self)

    # Redraws everything on the surface
    def redrawAll(self, screen):
        if (self.activeMode == 'menu'):
            self.drawMenu(screen)

        if (self.activeMode == 'game'):
            self.drawGame(screen)

    # Draws the Game Mode components
    def drawGame(self, screen):
        self.drawBoard(screen)
        self.drawGUI(screen)
    
    # Draws the Menu Mode Components
    def drawMenu(self, screen):
        for element in self.elements:
            element.draw(screen)

    # Checks if given position is within the bounds.
    def inBounds(self, pos, bounds):
        x, y = pos
        x0, y0, x1, y1 = bounds
        return (x > x0 and x < x1 and y > y0 and y < y1)
    
    # Draws the GUI Components of the Game Mode
    def drawGUI(self, screen):
        for element in self.elements:
            element.draw(screen)
        for key in self.buildElements:
            self.buildElements[key].draw(screen)
        if (self.inBuildMode):
            for selectElement in self.selectElements:
                selectElement.draw(screen)
        self.drawCurrentPlayer(screen)
        self.drawResources(screen)
    
    # Draws the resource panel at the bottom of the screen
    def drawResources(self, screen):
        x, y = windowConfig.RESOURCES
        width, height = windowConfig.RESOURCES_SIZE
        pygame.draw.rect(screen, Colors.BLACK, (x, y, width, height), 1)
        resources = self.board.players[self.currentPlayer].resources
        resourceText = f"{resources['lumber']} Lumber, {resources['brick']} Brick, {resources['sheep']} Sheep, {resources['grain']} Grain, {resources['ore']} Ore"
        resourceLabel = Text.RESOURCE_FONT.render(resourceText, True, Colors.BLACK)
        resourceSurf = resourceLabel.get_rect()
        resourceSurf.center = pygame.Rect(x, y, width, height).center
        screen.blit(resourceLabel, resourceSurf)

    # Draws the current player's on the screen
    def drawCurrentPlayer(self, screen):
        currentPlayer = self.currentPlayer + 1
        currentPlayerText = Text.CURRENT_PLAYER_FONT.render(f'Player {currentPlayer}\'s Turn', True, Colors.BLACK)
        currentPlayerSurf = currentPlayerText.get_rect()
        currentPlayerSurf.left = windowConfig.CURRENT_PLAYER[0]
        currentPlayerSurf.centery = windowConfig.CURRENT_PLAYER[1]
        screen.blit(currentPlayerText, currentPlayerSurf)

    # Draws the Catan Board
    def drawBoard(self, screen):
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
                leftOffset = ((self.board.q - rowLen) / 2) * self.hexWidth + self.boardBounds[0]
                x0 = leftOffset + j * self.hexWidth
                x1 = leftOffset + (j + 1) * self.hexWidth
                y0 = i * self.ySpacing + self.boardBounds[1]
                y1 = y0 + self.hexHeight
                center = (int(x0 + (x1-x0)/2), int(y0 + (y1-y0)/2))
                hexPoints = CatanMath.getHexagonPoints((x0, y0, x1, y1))
                pygame.draw.polygon(screen, hexFill, hexPoints)
                self.drawPorts(screen, (i, j+firstIndex), hexPoints, center)
                gfxdraw.aapolygon(screen, hexPoints, Colors.BLACK)
                self.drawTokens(screen, self.hexHeight, (i, j+firstIndex), center)
                self.drawRoads(screen, tile, hexPoints)
                self.drawNodes(screen, self.hexHeight, tile, hexPoints)

    # Draws Roads on the Catan Board
    def drawRoads(self, screen, tile, hexPoints):
        edgeIndex = 0
        for edge in tile.edges:
            edgeID = edge.id
            roadEdge = self.board.edges[edgeID]
            if (roadEdge.road != None):
                point1 = hexPoints[edgeIndex]
                point2 = hexPoints[(edgeIndex+1)%6]
                roadOwner = roadEdge.road
                roadArgs = CatanMath.getThickAALine(point1, point2)
                gfxdraw.filled_polygon(screen, roadArgs, roadOwner)
                gfxdraw.aapolygon(screen, roadArgs, roadOwner)
            edgeIndex += 1

    # Draws Nodes on the Catan Board
    def drawNodes(self, screen, hexHeight, tile, hexPoints):
        nodeIndex = 0
        nodeSize = int(0.1 * hexHeight)
        for node in tile.nodes:
            center = hexPoints[nodeIndex]
            if (node.pos == None):
                node.pos = center
            if (node.nodeLevel != 0):
                number = node.nodeLevel
                cx, cy = center
                cx, cy = int(cx), int(cy)
                pygame.draw.circle(screen, node.owner.bgColor, (cx, cy), nodeSize)
                gfxdraw.aacircle(screen, cx, cy, nodeSize, Colors.BLACK)
                nodeText = Text.NODE_FONT.render(str(number), True, node.owner.textColor)
                nodeSurf = nodeText.get_rect()
                nodeSurf.center = (cx, cy)
                screen.blit(nodeText, nodeSurf)
            nodeIndex += 1

    # Draws Tokens on the Catan Board
    def drawTokens(self, screen, hexHeight, pos, center):
        i, j = pos
        tokenSize = int(0.17 * hexHeight)
        number = self.board.hexBoard[i][j].number
        if (number != None):
            active = self.dice1.value + self.dice2.value
            color = Colors.WHITE
            if (number == active):
                color = Colors.GOLD_1
            pygame.draw.circle(screen, color, center, tokenSize)
            gfxdraw.aacircle(screen, center[0], center[1], tokenSize, Colors.BLACK)
            if (number in [6, 8]):
                tokenColor = Colors.BLACK
            else:
                tokenColor = Colors.BLACK
            token = Text.TOKEN_FONT.render(str(number), True, tokenColor)
            tokenSurf = token.get_rect()
            tokenSurf.center = center
            screen.blit(token, tokenSurf)
    
    # Draws Ports on the Catan Board
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
                portText = self.getPortContents(portIndex)
                portLabel = Text.PORT_FONT.render(portText, True, Colors.BLACK)
                portSurf = portLabel.get_rect()
                portSurf.center = (cx, cy)
                screen.blit(portLabel, portSurf)
            portIndex += 1
    
    # Gets the contents of the Port Token
    def getPortContents(self, portIndex):
        port = self.board.ports[portIndex]
        ports = {'wildcard':'? 3:1', 'lumber':'L 2:1', 'sheep':'S 2:1',
                'grain':'G 2:1', 'brick':'B 2:1', 'ore':'O 2:1'}
        return ports[port]
    
    # Gets the fill of each hex depending on the Tile type
    def getFill(self, tile):
        colors = {'forest':Colors.FOREST, 'desert':Colors.DESERT,
                  'hills':Colors.HILLS, 'mountains':Colors.MOUNTAINS,
                  'pasture':Colors.PASTURE, 'fields':Colors.FIELDS,
                  None:Colors.WHITE}
        tileFill = colors[tile.type]
        return tileFill

CatanGame(width=windowConfig.WIDTH, height=windowConfig.HEIGHT, title='Catan: The Settlers of Python').run()