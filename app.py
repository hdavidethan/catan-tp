#########################################################################
# App File
# Contains the main functions for the Catan Game
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

import pygame, copy, random
from pygame import gfxdraw
from pygameFramework import PygameGame
from resources.gui.button import Button
from resources.game.board import Board
from resources.game.utils import CatanMath
from resources.game.utils import Utils
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
        self.discardMode = False
        self.inRobberMode = False
        self.stealMode = False
        self.toDiscard = []
        self.auxPlayer = None
        self.board = Board()
        self.turn = 0
        self.dice1 = Dice(self, windowConfig.DICE_1, windowConfig.DICE_SIZE, 0)
        self.dice2 = Dice(self, windowConfig.DICE_2, windowConfig.DICE_SIZE, 1)
        self.currentPlayer = 0

    # Sets the active mode of the app
    def setActiveMode(self, mode):
        if (mode == 'menu'):
            self.initMenu()
            self.activeMode = 'menu'
        elif (mode == 'setup'):
            self.initSetup()
            self.activeMode = 'setup'
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
        self.oldRobberPos = None
        self.toDiscard = []
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
        self.discardElements = dict()
        self.stealElements = dict()
        self.initDiscardElements()
        self.initStealElements()
        self.initRoadsWrapper()
        self.setupMode = True
        players1 = [i for i in range(4, 8)]
        players2 = [i for i in range(4)]
        self.setupPlayOrder = players2 + players1[::-1]
        self.startSetupTurn()

    def initDiscardElements(self):
        resources = ['lumber', 'brick', 'sheep', 'grain', 'ore']
        for resource in resources:
            discardButton = Button(windowConfig.DISCARD[resource], windowConfig.DISCARD_SIZE, 'X', Colors.BUTTON_COLORS, ('discard', resource), 0.4, font=Text.DISCARD_FONT)
            self.discardElements[resource] = discardButton

    def initStealElements(self):
        for i in range(4):
            stealButton = Button(windowConfig.STEAL[i], windowConfig.STEAL_SIZE, 'Steal', Colors.BUTTON_COLORS, ('stealConfirm', self.board.players[i]), 0.4, font=Text.STEAL_FONT)
            self.stealElements[i] = stealButton

    # Starts the turn during the Set-up Phase
    def startSetupTurn(self):
        if (len(self.setupPlayOrder) > 0):
            self.turn = self.setupPlayOrder.pop()
            self.currentPlayer = self.turn % 4
            player = self.board.players[self.turn % 4]
            self.checkBuildConditions(player)
        else:
            self.setupMode = False
            self.dice1.roll()
            self.dice2.roll()
            self.startTurn()
    
    # Wrapper to initialize road positions
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
                if (tile.bounds == None):
                    tile.bounds = (x0, y0, x1, y1)
                hexPoints = CatanMath.getHexagonPoints((x0, y0, x1, y1))
                self.initRoads(tile, (x0, y0, x1, y1))

    # Initializes road positions         
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
    
    # Starts the turn
    def startTurn(self):
        self.dice1.roll()
        self.dice2.roll()
        roll = self.dice1.value + self.dice2.value
        if (roll == 7):
            self.sevenHandler()
        else:
            self.collectResources()
        turn = self.currentPlayer
        player = self.board.players[turn]
        self.checkBuildConditions(player)

    # Handles end turn clicks
    def endTurn(self):
        if (not self.setupMode):
            victory = self.checkVictory()
            if (victory != None):
                print(victory.index, 'wins!')
                self.setActiveMode('menu')
            else:    
                self.turn += 1
                self.currentPlayer = self.turn % 4
                self.startTurn()
        else:
            self.startSetupTurn()
    
    def checkVictory(self):
        for player in self.board.players:
            if (player.victoryPoints >= 10):
                return player
    
    # Collects resources for all players given current roll
    def collectResources(self):
        for i in range(self.board.q):
            row = copy.copy(self.board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = self.board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = self.board.hexBoard[i][j+firstIndex]
                if (tile.number == (self.dice1.value + self.dice2.value) and not tile.hasRobber):
                    for node in tile.nodes:
                        if (node.owner != None):
                            node.collectFromNumber(node.owner, tile.number, self.board)

    def sevenHandler(self):
        self.toDiscard = []
        for player in self.board.players:
            if (player.countCards() > 7):
                self.toDiscard.append(player.index)
        self.auxPlayer = self.currentPlayer
        if (len(self.toDiscard) > 0):
            self.startDiscard()
    
    def startDiscard(self):
        self.discardMode = True
        self.currentPlayer = self.toDiscard.pop(0)
        player = self.board.players[self.currentPlayer]
        player.discardGoal = player.countCards() // 2
        self.checkDiscardConditions(player)
        self.checkEndTurnConditions(player)
    
    def endDiscard(self):
        if (len(self.toDiscard) == 0):
            self.discardMode = False
            self.currentPlayer = self.auxPlayer
            self.robberMode()
        else:
            self.startDiscard()

    def discardResource(self, player, resource):
        player.resources[resource] -= 1
        self.checkDiscardConditions(player)
        self.checkEndTurnConditions(player)

    def checkDiscardConditions(self, player):
        for resource in player.resources:
            count = player.resources[resource]
            if (count < 1):
                self.discardElements[resource].isDisabled = True
            else:
                self.discardElements[resource].isDisabled = False

    # TODO: Make this recursive
    # i.e. do two halves and have each possible segment return a list of roads connected
    def checkLongestRoad(self, player):
        pass
    #     if (len(player.roads) >= 5):
    #         mainSet = copy.copy(player.roads)
    #         seen = set()
    #         first = random.choice(list(mainSet))
    #         mainSet.remove(first)
    #         seen.add(first)
    
    # def recursiveLongestRoad(self, player):
    #     if ():
    #         pass
    #     else:
    #         road1, road2 = first.getRoads(self.board)
    #         for edge in road1:
    #             if (self.board.edges[edge] in mainSet):
    #                 seen.add(self.board.edges[edge])
    #         for edge in road2:
    #             if (self.board.edges[edge] in mainSet):
    #                 seen.add(self.board.edges[edge])
            
    def checkEndTurnConditions(self, player):
        if ((self.discardMode and self.board.players[self.currentPlayer].countCards() > player.discardGoal) or self.inRobberMode or self.stealMode):
            tmpButton = Button(windowConfig.END_TURN, None, None, None, None)
            for element in self.elements:
                if (element == tmpButton):
                    element.isDisabled = True
        else:
            tmpButton = Button(windowConfig.END_TURN, None, None, None, None)
            for element in self.elements:
                if (element == tmpButton):
                    element.isDisabled = False

    # Checks build conditions and enables/disables the corresponding buttons
    def checkBuildConditions(self, player):
        roadCondition = (((not self.setupMode and player.resources['lumber'] >= 1 and player.resources['brick'] >= 1
                            and (len(player.settlements) + len(player.cities)) > 0) and not self.discardMode)
                            or (self.setupMode and (len(player.roads) < len(player.settlements))))
        settlementCondition = (((player.resources['lumber'] >= 1 and player.resources['brick'] >= 1
                            and player.resources['grain'] >= 1 and player.resources['sheep'] >= 1)
                            or (self.setupMode and ((self.turn // 4 == 1 and len(player.settlements) == 0) or
                            (self.turn // 4 == 0 and len(player.settlements) == 1)))) and not self.discardMode)
        cityCondition = ((player.resources['ore'] >= 3 and player.resources['grain'] >= 2
                            and len(player.settlements) > 0) and not self.discardMode)
        devCardCondition = ((not self.setupMode and player.resources['sheep'] >= 1 and player.resources['ore'] >= 1 
                            and player.resources['grain'] >= 1) and not self.discardMode)
        conditions = (('road', roadCondition), ('settlement', settlementCondition),
                    ('city', cityCondition), ('devCard', devCardCondition))
        for build in conditions:
            self.buildElements[build[0]].isDisabled = not build[1]
    
    # Handles the Build Mode logic
    def buildMode(self, build):
        self.inBuildMode = True
        self.selectElements = set()
        if (build == 'settlement'):
            for node in self.board.nodes:
                if (node.nodeLevel == 0 and node.buildable and (self.setupMode or node.checkOwnedRoads(self.board, self.board.players[self.currentPlayer]))):
                    cx, cy = node.pos
                    nodeButton = Button((cx, cy), windowConfig.SELECT_BUTTON_SIZE,
                            None, Colors.BUTTON_COLORS, ('buildConfirm', (node, self.board.players[self.currentPlayer])), 0.4)
                    self.selectElements.add(nodeButton)
        elif (build == 'city'):
            for node in self.board.nodes:
                if (node.nodeLevel == 1 and node.owner.index == self.currentPlayer):
                    cx, cy = node.pos
                    nodeButton = Button((cx, cy), windowConfig.SELECT_BUTTON_SIZE,
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
                        roadButton = Button((cx, cy), windowConfig.SELECT_BUTTON_SIZE,
                            None, Colors.BUTTON_COLORS, ('buildConfirm', (edge, self.board.players[self.currentPlayer])), 0.4)
                        self.selectElements.add(roadButton)

    def robberMode(self):
        self.inRobberMode = True
        self.selectElements = set()
        for i in range(self.board.q):
            row = copy.copy(self.board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = self.board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = self.board.hexBoard[i][j+firstIndex]
                if (not tile.hasRobber):
                    x0, y0, x1, y1 = tile.bounds
                    hexHeight = y1 - y0
                    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                    tileButton = Button((cx, cy + 0.25 * hexHeight), windowConfig.SELECT_BUTTON_SIZE,
                        None, Colors.BUTTON_COLORS, ('placeRobber', (tile, self.board.players[self.currentPlayer])), 0.4)
                    self.selectElements.add(tileButton)
                else:
                    self.oldRobberPos = (i, j+firstIndex)

    def stealChoice(self, stealInput):
        self.inRobberMode = False
        self.stealMode = True
        self.checkEndTurnConditions(self.board.players[self.currentPlayer])
        tile, player = stealInput
        victims = set()
        for node in tile.nodes:
            nodeID = node.id
            owner = self.board.nodes[nodeID].owner
            if (owner != None and owner != player and owner.countCards() > 0):
                victims.add(owner.index)
        if (len(victims) > 0):
            for key in self.stealElements:
                if (key in victims):
                    self.stealElements[key].isDisabled = False
                else:
                    self.stealElements[key].isDisabled = True
        else:
            self.stealMode = False
            self.checkEndTurnConditions(self.board.players[self.currentPlayer])

    # Checks for total victory points of the current player.
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
            for key in self.discardElements:
                x0, y0, width, height = self.discardElements[key].getRectArgs()
                x1 = x0 + width
                y1 = y0 + height
                if (mx > x0 and mx < x1 and my > y0 and my < y1):
                    self.discardElements[key].onClick(self)
            for key in self.stealElements:
                x0, y0, width, height = self.stealElements[key].getRectArgs()
                x1 = x0 + width
                y1 = y0 + height
                if (mx > x0 and mx < x1 and my > y0 and my < y1):
                    self.stealElements[key].onClick(self)

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
        bgImage = pygame.image.load("resources/assets/images/bgCatan.jpg")
        bgPos = bgImage.get_rect()
        bgPos.center = (self.cx, self.cy)
        screen.blit(bgImage, bgPos)
        logoImage = pygame.image.load("resources/assets/images/logoCatan.png")
        logoWidth, logoHeight = logoImage.get_rect().size
        scaleFactor = windowConfig.LOGO_SCALE
        logoImage = pygame.transform.scale(logoImage, (int(scaleFactor * logoWidth), int(scaleFactor * logoHeight)))
        logoPos = logoImage.get_rect()
        logoPos.center = windowConfig.LOGO
        screen.blit(logoImage, logoPos)
        x, y = windowConfig.MENU_CONTAINER
        width, height = windowConfig.MENU_CONTAINER_SIZE
        container = pygame.Surface((width, height), pygame.SRCALPHA)
        container.fill(Colors.BLACK_ALPHA)
        screen.blit(container, (x, y))
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
        if (self.inBuildMode or self.inRobberMode):
            for selectElement in self.selectElements:
                selectElement.draw(screen)
        if (self.discardMode):
            for key in self.discardElements:
                self.discardElements[key].draw(screen)
        if (self.stealMode):
            for key in self.stealElements:
                self.stealElements[key].draw(screen)
        self.drawCurrentPlayer(screen)
        self.drawResources(screen)
    
    # Draws the resource panel at the bottom of the screen
    def drawResources(self, screen):
        x, y = windowConfig.RESOURCES
        width, height = windowConfig.RESOURCES_SIZE
        pygame.draw.rect(screen, Colors.WHITE, (x, y, width, height))
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
        if (self.discardMode):
            player = self.board.players[self.currentPlayer]
            remaining = player.countCards() - player.discardGoal
            currentPlayerText = Text.CURRENT_PLAYER_FONT.render(f'Player {currentPlayer} Must Discard {remaining} Cards!', True, Colors.RED_1)
        elif (self.inRobberMode):
            currentPlayerText = Text.CURRENT_PLAYER_FONT.render(f'Player {currentPlayer} Must Move the Robber!', True, Colors.RED_1)
        elif (self.stealMode):
            currentPlayerText = Text.CURRENT_PLAYER_FONT.render(f'Player {currentPlayer} May Steal!', True, Colors.RED_1)
        else:
            currentPlayerText = Text.CURRENT_PLAYER_FONT.render(f'Player {currentPlayer}\'s Turn', True, Colors.BLACK)
        
        currentPlayerSurf = currentPlayerText.get_rect()
        currentPlayerSurf.right = windowConfig.CURRENT_PLAYER[0]
        currentPlayerSurf.centery = windowConfig.CURRENT_PLAYER[1]
        screen.blit(currentPlayerText, currentPlayerSurf)

    # Draws the Catan Board
    def drawBoard(self, screen):
        pygame.draw.rect(screen, Colors.BLUE, (0,0,self.width,self.height))
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
        hasRobber = self.board.hexBoard[i][j].hasRobber
        if (number != None):
            active = self.dice1.value + self.dice2.value
            color = Colors.WHITE
            if (number == active and not hasRobber):
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
        if (hasRobber):
            robberLabel = Text.ROBBER_FONT.render('R', True, Colors.RED_2)
            robberPos = robberLabel.get_rect()
            robberPos.centerx = center[0]
            robberPos.centery = center[1] + 0.3 * hexHeight
            screen.blit(robberLabel, robberPos)
    
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
                gfxdraw.aapolygon(screen, triangle, Colors.GOLD_2)
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