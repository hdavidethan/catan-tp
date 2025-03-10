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
from resources.game.aiplayer import AIPlayer
from resources.gui.dice import Dice
from resources.gui.scorecard import Scorecard
from config.colors import Colors
from config.config import windowConfig
from config.text import Text

class CatanGame(PygameGame):
    #################################################
    # PYGAME INIT METHODS AND MODE LOGIC
    #################################################

    # Run on app init
    def init(self):
        self.cx, self.cy = self.width/2, self.height/2
        self.boardSize = min(self.width*0.65, self.height*0.65)
        x0 = self.cx - self.boardSize / 2
        y0 = self.cy - (self.boardSize / windowConfig.HEIGHT_TO_WIDTH_RATIO) / 2
        x1 = self.cx + self.boardSize / 2
        y1 = self.cy + (self.boardSize / windowConfig.HEIGHT_TO_WIDTH_RATIO) / 2
        self.boardBounds = (x0, y0, x1, y1)
        self.hexWidth = self.boardSize / 5
        self.hexHeight = self.boardSize / 4
        self.ySpacing = self.hexHeight * 3 / 4
        self.activeMode = None
        self.isPaused = False
        self.victoryMode = False
        self.humanCount = 2
        self.aiCount = 2
        self.fogOfWar = True
        self.imageCache = dict()
        self.soundCache = dict()
        self.initAudio()
        self.setActiveMode('menu')
    
    # Initializes the Audio objects
    def initAudio(self):
        pygame.mixer.music.load('resources/assets/audio/catan.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)
        self.musicPaused = False
        self.soundCache['buttonClick'] = pygame.mixer.Sound('resources/assets/audio/button.ogg')
        self.soundCache['buttonClick'].set_volume(0.7)

    # Loads an image into an image cache and returns the cached image
    def loadImageFromCache(self, path):
        if path not in self.imageCache:
            image = pygame.image.load(path)
            self.imageCache[path] = image
        return self.imageCache[path]

    # Resets all game variables (Board, Player, etc.)
    def resetGame(self, human, ai):
        self.inBuildMode = False
        self.fogOfWar = True if human > 0 else False
        self.discardMode = False
        self.inRobberMode = False
        self.stealMode = False
        self.devCardMode = False
        self.yearOfPlentyMode = False
        self.isPaused = False
        self.victoryMode = False
        self.toDiscard = []
        self.auxPlayer = None
        self.board = Board(human=human, ai=ai)
        self.turn = 0
        self.dice1 = Dice(self, windowConfig.DICE_1, windowConfig.DICE_SIZE, 0)
        self.dice2 = Dice(self, windowConfig.DICE_2, windowConfig.DICE_SIZE, 1)
        self.currentPlayer = 0

    # Sets the active mode of the app
    def setActiveMode(self, mode, human=4, ai=0):
        if (mode == 'menu'):
            self.initMenu()
            self.activeMode = 'menu'
        elif (mode == 'setup'):
            self.initSetup()
            self.activeMode = 'setup'
        elif (mode == 'game'):
            self.initGame(human, ai)
            self.activeMode = 'game'

    # Runs upon Menu Mode activation/switch
    def initMenu(self):
        self.isPaused = False
        self.elements = set()
        menuButton1 = Button(windowConfig.MENU_B1,windowConfig.MENU_SIZE,
            'New Game', Colors.BUTTON_COLORS, ('changeMode', 'setup'), 0.4)
        menuButton2 = Button(windowConfig.MENU_B2, windowConfig.MENU_SIZE,
            'Quit Game', Colors.BUTTON_COLORS, ('quit', None), 0.4)
        self.elements.add(menuButton1)
        self.elements.add(menuButton2)

    # Runs upon Setup Mode activation/switch
    def initSetup(self):
        self.elements = set()
        humanPlus = Button(windowConfig.SETUP_HUMAN_INC, windowConfig.SETUP_INC_DEC_SIZE, 
            '+', Colors.BUTTON_COLORS, ('humanIncDec', +1), 0.4, font=Text.INC_DEC_FONT)
        humanMinus = Button(windowConfig.SETUP_HUMAN_DEC, windowConfig.SETUP_INC_DEC_SIZE,
            '-', Colors.BUTTON_COLORS, ('humanIncDec', -1), 0.4, font=Text.INC_DEC_FONT)
        aiPlus = Button(windowConfig.SETUP_AI_INC, windowConfig.SETUP_INC_DEC_SIZE, '+',
            Colors.BUTTON_COLORS, ('aiIncDec', +1), 0.4, font=Text.INC_DEC_FONT)
        aiMinus = Button(windowConfig.SETUP_AI_DEC, windowConfig.SETUP_INC_DEC_SIZE, '-',
            Colors.BUTTON_COLORS, ('aiIncDec', -1), 0.4, font=Text.INC_DEC_FONT)
        setupConfirm = Button(windowConfig.SETUP_CONFIRM, windowConfig.SETUP_CONFIRM_SIZE,
            'Start Game', Colors.BUTTON_COLORS, ('setupConfirm', None), 0.4)
        self.elements.add(humanPlus)
        self.elements.add(humanMinus)
        self.elements.add(aiPlus)
        self.elements.add(aiMinus)
        self.elements.add(setupConfirm)
        self.checkHumanCount()
        self.checkAICount()
        self.checkSetupConfirm()

    # Runs upon Game Mode activation/switch
    def initGame(self, human, ai):
        self.resetGame(human, ai)
        self.oldRobberPos = None
        self.toDiscard = []
        self.elements = set()
        self.selectElements = set()
        self.playerCount = human + ai
        scores = [windowConfig.SCORE_1, windowConfig.SCORE_2,
            windowConfig.SCORE_3, windowConfig.SCORE_4]
        scoreCounter = 0
        for player in self.board.players:
            self.elements.add(Scorecard(player, scores[scoreCounter],
                windowConfig.SCORE_SIZE))
            scoreCounter += 1
        endTurnButton = Button(windowConfig.END_TURN, windowConfig.END_TURN_SIZE,
            'End Turn', Colors.BUTTON_COLORS, ('endTurn', None), 0.4)
        useDevCardButton = Button(windowConfig.USE_DEVCARD, windowConfig.USE_DEVCARD_SIZE,
            'Use Dev Card', Colors.BUTTON_COLORS, ('devCard', None), 0.4, True, Text.BUILD_FONT)
        self.elements.add(endTurnButton)
        self.elements.add(useDevCardButton)
        self.elements.add(self.dice1)
        self.elements.add(self.dice2)
        self.buildElements = dict()
        self.discardElements = dict()
        self.devCardElements = dict()
        self.stealElements = dict()
        self.yearOfPlentyElements = dict()
        self.pauseElements = set()
        self.victoryElements = set()
        self.initBuildElements()
        self.initDiscardElements()
        self.initDevCardElements()
        self.initStealElements()
        self.initYearOfPlentyElements()
        self.initPauseElements()
        self.initVictoryElements()
        self.initRoadsWrapper()
        self.setupMode = True
        players1 = [i for i in range(self.playerCount, self.playerCount*2)]
        players2 = [i for i in range(self.playerCount)]
        self.setupPlayOrder = players2 + players1[::-1]
        self.startSetupTurn()

    # Initializes the build button elements on the left side of the screen.
    def initBuildElements(self):
        builds = ['road', 'settlement', 'city', 'devCard']
        for build in builds:
            buildButton = Button(windowConfig.BUILD[build], windowConfig.BUILD_SIZE, 
                                Text.BUILD[build], Colors.BUTTON_COLORS, ('build', build), 0.4, font=Text.BUILD_FONT)
            self.buildElements[build] = buildButton

    # Initializes the discard button elements for Discard Mode
    def initDiscardElements(self):
        resources = Utils.RESOURCES
        for resource in resources:
            discardButton = Button(windowConfig.DISCARD[resource], windowConfig.DISCARD_SIZE, 
                                'X', Colors.BUTTON_COLORS, ('discard', resource), 0.4, font=Text.DISCARD_FONT)
            self.discardElements[resource] = discardButton

    # Initializes year of plenty buttons
    def initYearOfPlentyElements(self):
        resources = Utils.RESOURCES
        for resource in resources:
            claimButton = Button(windowConfig.DISCARD[resource], windowConfig.DISCARD_SIZE, 
                                '+', Colors.BUTTON_COLORS, ('claim', resource), 0.4, font=Text.DISCARD_FONT)
            self.yearOfPlentyElements[resource] = claimButton

    # Initializes the steal button elements for the Steal Mode
    def initStealElements(self):
        for i in range(self.playerCount):
            stealButton = Button(windowConfig.STEAL[i], windowConfig.STEAL_SIZE,
                                'Steal', Colors.BUTTON_COLORS, ('stealConfirm', self.board.players[i]), 0.4, font=Text.STEAL_FONT)
            self.stealElements[i] = stealButton

    # Initializes the button elements for the Pause Mode
    def initPauseElements(self):
        resumeButton = Button(windowConfig.PAUSE_RESUME, windowConfig.PAUSE_SIZE,
            'Resume Game', Colors.BUTTON_COLORS, ('pause', None), 0.4, isPauseButton=True)
        restartButton = Button(windowConfig.PAUSE_RESTART, windowConfig.PAUSE_SIZE,
            'Restart Game', Colors.BUTTON_COLORS, ('restart', None), 0.4, isPauseButton=True)
        quitButton = Button(windowConfig.PAUSE_QUIT, windowConfig.PAUSE_SIZE,
            'Exit to Menu', Colors.BUTTON_COLORS, ('changeMode', 'menu'), 0.4, isPauseButton=True)
        self.pauseElements.add(resumeButton)
        self.pauseElements.add(restartButton)
        self.pauseElements.add(quitButton)

    # Initializes the button elements for the Victory Mode
    def initVictoryElements(self):
        restartButton = Button(windowConfig.VICTORY_RESTART, windowConfig.PAUSE_SIZE,
            'Rematch', Colors.BUTTON_COLORS, ('restart', None), 0.4, isPauseButton=True)
        quitButton = Button(windowConfig.VICTORY_QUIT, windowConfig.PAUSE_SIZE,
            'Exit to Menu', Colors.BUTTON_COLORS, ('changeMode', 'menu'), 0.4, isPauseButton=True)
        self.victoryElements.add(restartButton)
        self.victoryElements.add(quitButton)

    # Initializes the discard button elements for Discard Mode
    def initDevCardElements(self):
        devCards = ['knight', 'yearOfPlenty']
        for devCard in devCards:
            devCardButton = Button(windowConfig.DEVCARD_CHOICE[devCard],
                                windowConfig.DEVCARD_CHOICE_SIZE, '*', Colors.BUTTON_COLORS,
                                ('confirmDevCard', (devCard, None)), 0.4, font=Text.DISCARD_FONT)
            self.devCardElements[devCard] = devCardButton
    
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
    
    #################################################
    # CATAN GAME TURN LOGIC
    #################################################

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
        if (isinstance(player, AIPlayer)):
            player.startTurn(self)
        else:
            self.checkForLongestRoad()
            self.checkForLargestArmy()
            self.checkBuildConditions(player)
            self.useDevCardConditions(player)

    # Starts the turn during the Set-up Phase
    def startSetupTurn(self):
        if (len(self.setupPlayOrder) > 0):
            self.turn = self.setupPlayOrder.pop()
            self.currentPlayer = self.turn % self.playerCount
            player = self.board.players[self.currentPlayer]
            if (isinstance(player, AIPlayer)):
                player.startTurn(self)
            else:
                self.checkBuildConditions(player)
        else:
            self.setupMode = False
            self.dice1.roll()
            self.dice2.roll()
            self.startTurn()

    # Handles end turn clicks
    def endTurn(self):
        if (not self.setupMode):
            victory = self.checkVictory()
            if (victory != None):
                self.victoryMode = True
            else:    
                self.turn += 1
                self.currentPlayer = self.turn % self.playerCount
                self.startTurn()
        else:
            self.startSetupTurn()
    
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

    # Handles switching to Robber Mode and Steal Mode when a 7 is rolled.
    def sevenHandler(self):
        self.toDiscard = []
        for player in self.board.players:
            if (player.countCards() > 7):
                self.toDiscard.append(player.index)
        self.auxPlayer = self.currentPlayer
        if (len(self.toDiscard) > 0):
            self.startDiscard()
        else:
            self.discardMode = False
            self.currentPlayer = self.auxPlayer
            self.robberMode()
    
    # Starts the round of discarding extra cards when 7 is rolled.
    def startDiscard(self):
        self.discardMode = True
        self.currentPlayer = self.toDiscard.pop(0)
        player = self.board.players[self.currentPlayer]
        player.discardGoal = player.countCards() // 2
        self.checkDiscardConditions(player)
        self.checkEndTurnConditions(player)
        if (isinstance(player, AIPlayer)):
            player.startDiscard(self)
    
    # Starts the year of plenty claim round
    def startYearOfPlenty(self):
        self.yearOfPlentyMode = True
        player = self.board.players[self.currentPlayer]
        player.discardGoal = player.countCards() + 2
        self.checkYearOfPlentyConditions(player)
        self.checkEndTurnConditions(player)
        if (isinstance(player, AIPlayer)):
            player.startYearOfPlenty(self)

    # Starts the development card phase
    def startDevCard(self):
        self.devCardMode = True
        player = self.board.players[self.currentPlayer]
        self.devCardChoiceConditions(player)
    
    # Ends the discard turn or discard round.
    def endDiscard(self):
        if (len(self.toDiscard) != 0):
            self.startDiscard()
        else:
            self.discardMode = False
            self.currentPlayer = self.auxPlayer
            self.robberMode()

    # Removes one of the given resource from the player and update information
    def discardResource(self, player, resource):
        player.resources[resource] -= 1
        self.checkDiscardConditions(player)
        self.checkEndTurnConditions(player)
    
    # Add one of the given resource from the player and update information
    def claimResource(self, player, resource):
        player.resources[resource] += 1
        self.checkYearOfPlentyConditions(player)
        self.checkEndTurnConditions(player)
    
    # Handles the Build Mode logic
    def buildMode(self, build):
        self.inBuildMode = True
        self.selectElements = set()
        if (build == 'settlement'):
            for node in self.board.nodes:
                validNode = node.checkOwnedRoads(self.board, self.board.players[self.currentPlayer])
                if (node.nodeLevel == 0 and node.buildable and (self.setupMode or validNode)):
                    cx, cy = node.pos
                    nodeButton = Button((cx, cy), windowConfig.SELECT_BUTTON_SIZE,
                            None, Colors.SELECT_BUTTON_COLORS, ('buildConfirm', 
                            (node, self.board.players[self.currentPlayer])), 0.4)
                    self.selectElements.add(nodeButton)
        elif (build == 'city'):
            for node in self.board.nodes:
                if (node.nodeLevel == 1 and node.owner.index == self.currentPlayer):
                    cx, cy = node.pos
                    nodeButton = Button((cx, cy), windowConfig.SELECT_BUTTON_SIZE,
                            None, Colors.SELECT_BUTTON_COLORS, ('buildConfirm', 
                            (node, self.board.players[self.currentPlayer])), 0.4)
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
                    ownedRoads = set()
                    found = False
                    for i in roads:
                        if (self.board.edges[i].road == self.board.players[self.currentPlayer].bgColor):
                            found = True
                            ownedRoads.add(self.board.edges[i])
                            tmp.remove(i)
                    if (found == True):
                        for i in tmp:
                            checkRoad = self.board.edges[i]
                            for ownedRoad in ownedRoads:
                                adjacent, tile = ownedRoad.checkAdjacent(checkRoad, self.board)
                                if (adjacent):
                                    ownedIndex = tile.edges.index(ownedRoad)
                                    checkIndex = tile.edges.index(checkRoad)
                                    if (ownedIndex > checkIndex):
                                        nodeIndex = ownedIndex
                                    else:
                                        nodeIndex = checkIndex
                                    nodeID = tile.nodes[nodeIndex].id
                                    adjNode = self.board.nodes[nodeID]
                                    if (adjNode.owner in [None, self.board.players[self.currentPlayer]]):
                                        seen.add(i)
                for i in seen:
                    edge = self.board.edges[i]
                    if (edge.road == None):
                        cx, cy = edge.pos
                        roadButton = Button((cx, cy), windowConfig.SELECT_BUTTON_SIZE,
                            None, Colors.SELECT_BUTTON_COLORS, ('buildConfirm', 
                            (edge, self.board.players[self.currentPlayer])), 0.4)
                        self.selectElements.add(roadButton)
        elif (build == 'devCard'):
            devCards = ['knight'] * 14 + ['yearOfPlenty'] * 2 + ['victoryPoint'] * 5 # ['roadBuilding'] * 2 + ['monopoly'] * 2 + 
            chosenCard = random.choice(devCards)
            devCards.remove(chosenCard)
            player = self.board.players[self.currentPlayer]
            player.resources['grain'] -= 1
            player.resources['sheep'] -= 1
            player.resources['ore'] -= 1
            player.devCards[chosenCard] += 1
            self.checkBuildConditions(player)
            self.useDevCardConditions(player)

    # Starts the Robber Mode and checks possible robber positions.
    def robberMode(self):
        player = self.board.players[self.currentPlayer]
        self.devCardMode = False
        self.inRobberMode = True
        self.checkEndTurnConditions(player)
        self.selectElements = set()
        aiSet = set()
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
                    if (not isinstance(player, AIPlayer)):
                        x0, y0, x1, y1 = tile.bounds
                        hexHeight = y1 - y0
                        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                        tileButton = Button((cx, cy + 0.25 * hexHeight), windowConfig.SELECT_BUTTON_SIZE,
                            None, Colors.SELECT_BUTTON_COLORS, ('placeRobber', (tile, player)), 0.4)
                        self.selectElements.add(tileButton)
                    else:
                        aiSet.add(tile)
                else:
                    self.oldRobberPos = (i, j+firstIndex)
        if (isinstance(player, AIPlayer)):
            player.robberMode(self, aiSet)

    # Handles Steal Mode. Gives choice for steal when more than 1 is possible.
    def stealChoice(self, stealInput):
        tile, player = stealInput
        self.inRobberMode = False
        self.selectElements = set()
        self.stealMode = True
        self.checkEndTurnConditions(player)
        victims = set()
        for node in tile.nodes:
            nodeID = node.id
            owner = self.board.nodes[nodeID].owner
            if (owner != None and owner != player and owner.countCards() > 0):
                victims.add(owner.index)
        if (len(victims) > 0):
            if (isinstance(player, AIPlayer)):
                player.stealChoice(self, victims)
            else:
                for key in self.stealElements:
                    if (key in victims):
                        self.stealElements[key].isDisabled = False
                    else:
                        self.stealElements[key].isDisabled = True
        else:
            self.stealMode = False
            self.checkBuildConditions(player)
            self.useDevCardConditions(player)
            self.checkEndTurnConditions(player)
    
    #################################################
    # CATAN GAME CONDITION LOGIC
    #################################################

    # Checks which player has the longest road
    def checkForLongestRoad(self):
        maxPlayer = None
        maxLength = -1
        for player in self.board.players:
            length = player.longestRoad
            if (length > maxLength):
                maxLength = length
                maxPlayer = player
        if (maxPlayer != None and maxLength >= 5):
            for player in self.board.players:
                if (player != maxPlayer):
                    player.hasLongestRoad = False
                else:
                    player.hasLongestRoad = True

    def checkForLargestArmy(self):
        maxPlayer = None
        maxAmount = -1
        for player in self.board.players:
            amount = player.largestArmy
            if (amount > maxAmount):
                maxAmount = amount
                maxPlayer = player
        if (maxPlayer != None and maxAmount >= 3):
            for player in self.board.players:
                if (player != maxPlayer):
                    player.hasLargestArmy = False
                else:
                    player.hasLargestArmy = True

    # Checks for total victory points of the current player.
    def checkVictoryPoints(self):
        player = self.board.players[self.currentPlayer]
        settlements = len(player.settlements)
        cities = len(player.cities)
        if (player.hasLongestRoad):
            longestRoad = 2
        else:
            longestRoad = 0
        if (player.hasLargestArmy):
            largestArmy = 2
        else:
            largestArmy = 0
        player.victoryPoints = settlements + 2 * cities + longestRoad + largestArmy

    # Checks if any player has achieved the VP threshold. Returns the player.
    def checkVictory(self):
        for player in self.board.players:
            if (player.victoryPoints + player.devCards['victoryPoint'] >= Utils.VICTORY_POINT_THRESHOLD):
                return player

    # Checks for the conditions to use each development card
    def useDevCardConditions(self, player):
        tmpButton = Button(windowConfig.USE_DEVCARD, None, None, None, None)
        total = 0
        for devCard in player.devCards:
            if (devCard != 'victoryPoint'):
                total += player.devCards[devCard]
        if (total > 0 and not isinstance(player, AIPlayer)):
            for element in self.elements:
                if (element == tmpButton):
                    element.isDisabled = False
        else:
            for element in self.elements:
                if (element == tmpButton):
                    element.isDisabled = True     

    # Checks for the conditions to use any development card
    def devCardChoiceConditions(self, player):
        conditions = []
        for devCard in player.devCards:
            if (devCard not in ['victoryPoint', 'monopoly', 'roadBuilding']):
                count = player.devCards[devCard]
                if (player.devCards[devCard] < 1):
                    self.devCardElements[devCard].isDisabled = True
                else:
                    self.devCardElements[devCard].isDisabled = False
                    conditions.append(devCard)
        return conditions

    # Checks if it is possible to discard certain resources. (i.e. is > 0)
    def checkDiscardConditions(self, player):
        resources = copy.copy(Utils.RESOURCES)
        for resource in player.resources:
            count = player.resources[resource]
            if (count < 1 or (player.countCards() <= player.discardGoal)):
                self.discardElements[resource].isDisabled = True
                resources.remove(resource)
            else:
                self.discardElements[resource].isDisabled = False
        return resources

    # Checks if the turn can be ended by the current player.
    def checkEndTurnConditions(self, player):
        discardCondition = self.discardMode and player.countCards() > player.discardGoal
        yearOfPlentyCondition = self.yearOfPlentyMode and player.countCards() < player.discardGoal
        inSubMode = self.inRobberMode or self.stealMode
        if (discardCondition or yearOfPlentyCondition or inSubMode):
            tmpButton = Button(windowConfig.END_TURN, None, None, None, None)
            for element in self.elements:
                if (element == tmpButton):
                    element.isDisabled = True
                    return False
        else:
            tmpButton = Button(windowConfig.END_TURN, None, None, None, None)
            for element in self.elements:
                if (element == tmpButton):
                    element.isDisabled = False
                    return True

    # Checks build conditions and enables/disables the corresponding buttons
    def checkBuildConditions(self, player):
        # Road Conditions
        settlementExists = (len(player.settlements) + len(player.cities)) > 0
        roadResources = (player.resources['lumber'] >= 1 and 
                            player.resources['brick'] >= 1)
        setupRoads = (self.setupMode and 
                    (len(player.roads) < len(player.settlements)))
        roadCondition = (((not self.setupMode and roadResources and 
                    settlementExists) and not self.discardMode) or setupRoads)
        # Settlement Conditions
        settlementResources = (player.resources['lumber'] >= 1 and player.resources['brick'] >= 1
                            and player.resources['grain'] >= 1 and player.resources['sheep'] >= 1)
        settlementCondition = ((settlementResources or (self.setupMode and
                            ((self.turn // self.playerCount == 1 and len(player.settlements) == 0) or
                            (self.turn // self.playerCount == 0 and len(player.settlements) == 1)))) and not self.discardMode)
        # City Conditions
        cityCondition = ((player.resources['ore'] >= 3 and player.resources['grain'] >= 2
                            and len(player.settlements) > 0) and not self.discardMode)
        # Dev Card Conditions
        devCardCondition = ((not self.setupMode and player.resources['sheep'] >= 1 and player.resources['ore'] >= 1 
                            and player.resources['grain'] >= 1) and not self.discardMode)
        # Compile conditions
        conditions = (('road', roadCondition), ('settlement', settlementCondition),
                    ('city', cityCondition), ('devCard', devCardCondition))
        for build in conditions:
            if (isinstance(player, AIPlayer)):
                self.buildElements[build[0]].isDisabled = True
            else:
                self.buildElements[build[0]].isDisabled = not build[1]
        return conditions

    # Checks if 2 resources have been claimed already.
    def checkYearOfPlentyConditions(self, player):
        for resource in Utils.RESOURCES:
            if (player.countCards() >= player.discardGoal):
                self.yearOfPlentyMode = False
                self.useDevCardConditions(player)
                self.checkBuildConditions(player)
            else:
                self.discardElements[resource].isDisabled = False

    #################################################
    # GAME SETUP CONDITION LOGIC
    #################################################

    # Checks if the number of human players is valid.
    def checkHumanCount(self):
        incElement = Button(windowConfig.SETUP_HUMAN_INC, None, None, None, None)
        decElement = Button(windowConfig.SETUP_HUMAN_DEC, None, None, None, None)
        for element in self.elements:
            if (element == incElement):
                if (self.humanCount + self.aiCount >= 4):
                    element.isDisabled = True
                else:
                    element.isDisabled = False
            elif (element == decElement):
                if (self.humanCount + self.aiCount <= 0 or self.humanCount <= 0):
                    element.isDisabled = True
                else:
                    element.isDisabled = False
    
    # Checks if the number of AI players is valid.
    def checkAICount(self):
        incElement = Button(windowConfig.SETUP_AI_INC, None, None, None, None)
        decElement = Button(windowConfig.SETUP_AI_DEC, None, None, None, None)
        for element in self.elements:
            if (element == incElement):
                if (self.humanCount + self.aiCount >= 4):
                    element.isDisabled = True
                else:
                    element.isDisabled = False
            elif (element == decElement):
                if (self.humanCount + self.aiCount <= 0 or self.aiCount <= 0):
                    element.isDisabled = True
                else:
                    element.isDisabled = False
    
    # Checks if the total number of players is valid.
    def checkSetupConfirm(self):
        confirmElement = Button(windowConfig.SETUP_CONFIRM, None, None, None, None)
        for element in self.elements:
            if (element == confirmElement):
                if (self.humanCount + self.aiCount > 4 or self.humanCount + self.aiCount < 2):
                    element.isDisabled = True
                else:
                    element.isDisabled = False

    #################################################
    # PYGAME FRAMEWORK CONTROLLERS
    #################################################

    # Handles keystrokes
    def keyPressed(self, key, mod):
        # Global Key Bindings
        if (key == pygame.K_F1):
            if (not self.musicPaused):
                pygame.mixer.music.pause()
                self.musicPaused = True
            else:
                pygame.mixer.music.unpause()
                self.musicPaused = False
        # Game Mode specific Key Bindings
        if (self.activeMode == 'game'):
            if (key == pygame.K_m):
                self.setActiveMode('menu')
            elif (key == pygame.K_r):
                self.setActiveMode('game')
            elif (key == pygame.K_c):
                for player in self.board.players:
                    player.resources[random.choice(['grain', 'lumber', 'ore', 'sheep', 'brick'])] += 1
            elif (key == pygame.K_1):
                player = self.board.players[self.currentPlayer]
                player.resources['lumber'] += 1
            elif (key == pygame.K_2):
                player = self.board.players[self.currentPlayer]
                player.resources['brick'] += 1
            elif (key == pygame.K_3):
                player = self.board.players[self.currentPlayer]
                player.resources['sheep'] += 1
            elif (key == pygame.K_4):
                player = self.board.players[self.currentPlayer]
                player.resources['grain'] += 1
            elif (key == pygame.K_5):
                player = self.board.players[self.currentPlayer]
                player.resources['ore'] += 1
            elif (key == pygame.K_ESCAPE):
                self.isPaused = not self.isPaused
            elif (key == pygame.K_y):
                self.board.players[self.currentPlayer].devCards['yearOfPlenty'] += 1
            elif (key == pygame.K_k):
                self.board.players[self.currentPlayer].devCards['knight'] += 1
            elif (key == pygame.K_F7):
                self.fogOfWar = not self.fogOfWar
            elif (key == pygame.K_v):
                self.victoryMode = True
            self.checkBuildConditions(self.board.players[self.currentPlayer])
            self.useDevCardConditions(self.board.players[self.currentPlayer])

    # Handles mouse presses
    def mousePressed(self, mx, my):
        for element in self.elements:
            self.clickBoxHandler(element, mx, my)
        if (self.activeMode == 'game'):
            for key in self.buildElements:
                self.clickBoxHandler(self.buildElements[key], mx, my)
            if (len(self.selectElements) > 0):
                for selectElement in self.selectElements:
                    self.clickBoxHandler(selectElement, mx, my)
            for key in self.discardElements:
                self.clickBoxHandler(self.discardElements[key], mx, my)
            for key in self.stealElements:
                self.clickBoxHandler(self.stealElements[key], mx, my)
            for key in self.devCardElements:
                self.clickBoxHandler(self.devCardElements[key], mx, my)
            if (self.yearOfPlentyMode):
                for key in self.yearOfPlentyElements:
                    self.clickBoxHandler(self.yearOfPlentyElements[key], mx, my)
            if (self.isPaused):
                for pauseElement in self.pauseElements:
                    self.clickBoxHandler(pauseElement, mx, my)
            if (self.victoryMode):
                for victoryElement in self.victoryElements:
                    self.clickBoxHandler(victoryElement, mx, my)
    
    # Checks if click was made inside the bounding box of the element
    def clickBoxHandler(self, element, mx, my):
        x0, y0, width, height = element.getRectArgs()
        x1 = x0 + width
        y1 = y0 + height
        if (mx > x0 and mx < x1 and my > y0 and my < y1):
            element.onClick(self)

    #################################################
    # PYGAME FRAMEWORK VIEW
    #################################################

    # Redraws everything on the surface
    def redrawAll(self, screen):
        if (self.activeMode == 'menu'):
            self.drawMenu(screen)
        if (self.activeMode == 'setup'):
            self.drawSetup(screen)
        if (self.activeMode == 'game'):
            self.drawGame(screen)

    # Draws the Game Mode components
    def drawGame(self, screen):
        self.drawBoard(screen)
        self.drawGUI(screen)
        if (self.isPaused):
            self.drawPaused(screen)
        elif (self.victoryMode):
            self.drawVictory(screen)
    
    # Draw the Pause Screen
    def drawPaused(self, screen):
        container = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        container.fill(Colors.BLACK_PAUSED)
        pausedText = Text.PAUSED_FONT.render('Game Paused', True, Colors.WHITE)
        pausedPos = pausedText.get_rect()
        pausedPos.center = (self.width / 2, self.height / 3)
        container.blit(pausedText, pausedPos)
        screen.blit(container, (0, 0))
        for pauseElement in self.pauseElements:
            pauseElement.draw(screen, self)

    # Draw the Victory Screen
    def drawVictory(self, screen):
        container = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        container.fill(Colors.BLACK_PAUSED)
        player = self.board.players[self.currentPlayer]
        playerType = 'COM Player' if isinstance(player, AIPlayer) else 'Player'
        currentPlayer = self.currentPlayer + 1
        victoryText = Text.VICTORY_FONT.render(f'{playerType} {currentPlayer} Wins!', True, Colors.WHITE)
        victoryPos = victoryText.get_rect()
        victoryPos.center = (self.width / 2, self.height / 3)
        container.blit(victoryText, victoryPos)
        screen.blit(container, (0, 0))
        for victoryElement in self.victoryElements:
            victoryElement.draw(screen, self)

    # Draws the Menu Mode Components
    def drawMenu(self, screen):
        self.drawBackground(screen)
        logoScale = windowConfig.LOGO_SCALE
        logoPos = windowConfig.LOGO
        self.drawLogo(screen, logoScale, logoPos)
        x, y = windowConfig.MENU_CONTAINER
        width, height = windowConfig.MENU_CONTAINER_SIZE
        container = pygame.Surface((width, height), pygame.SRCALPHA)
        container.fill(Colors.BLACK_ALPHA)
        screen.blit(container, (x, y))
        for element in self.elements:
            element.draw(screen, self)
    
    # Draws the Setup Mode Components
    def drawSetup(self, screen):
        self.drawBackground(screen)
        logoScale = windowConfig.LOGO_SCALE
        logoPos = windowConfig.LOGO
        self.drawLogo(screen, logoScale, logoPos)
        x, y = windowConfig.SETUP_CONTAINER
        width, height = windowConfig.SETUP_CONTAINER_SIZE
        container = pygame.Surface((width, height), pygame.SRCALPHA)
        container.fill(Colors.BLACK_ALPHA)
        screen.blit(container, (x, y))
        title = Text.SETUP_TITLE_FONT.render('Game Setup', True, Colors.WHITE)
        titlePos = title.get_rect()
        titlePos.center = windowConfig.SETUP_TITLE
        screen.blit(title, titlePos)
        humanLabel = Text.SETUP_LABEL_FONT.render('Human Players', True, Colors.WHITE)
        humanPos = humanLabel.get_rect()
        humanPos.center = windowConfig.SETUP_HUMAN
        screen.blit(humanLabel, humanPos)
        aiLabel = Text.SETUP_LABEL_FONT.render('AI Players', True, Colors.WHITE)
        aiPos = aiLabel.get_rect()
        aiPos.center = windowConfig.SETUP_AI
        screen.blit(aiLabel, aiPos)
        humans = self.humanCount
        humanCountLabel = Text.SETUP_COUNT_FONT.render(str(humans), True, Colors.WHITE)
        humanCountPos = humanCountLabel.get_rect()
        humanCountPos.center = windowConfig.SETUP_HUMAN_COUNT
        screen.blit(humanCountLabel, humanCountPos)
        ais = self.aiCount
        aiCountLabel = Text.SETUP_COUNT_FONT.render(str(ais), True, Colors.WHITE)
        aiCountPos = aiCountLabel.get_rect()
        aiCountPos.center = windowConfig.SETUP_AI_COUNT
        screen.blit(aiCountLabel, aiCountPos)
        for element in self.elements:
            element.draw(screen, self)

    # Draws the Catan Background
    def drawBackground(self, screen):
        bgImage = self.loadImageFromCache("resources/assets/images/bgCatan.jpg")
        bgPos = bgImage.get_rect()
        bgPos.center = (self.cx, self.cy)
        screen.blit(bgImage, bgPos)
    
    # Draws the Catan Logo
    def drawLogo(self, screen, scale, pos):
        logoImage = self.loadImageFromCache("resources/assets/images/logoCatan.png")
        logoWidth, logoHeight = logoImage.get_rect().size
        scaleFactor = scale
        logoImage = pygame.transform.scale(logoImage, (int(scaleFactor * logoWidth), int(scaleFactor * logoHeight)))
        logoPos = logoImage.get_rect()
        logoPos.center = pos
        screen.blit(logoImage, logoPos)

    # Draws the GUI Components of the Game Mode
    def drawGUI(self, screen):
        for element in self.elements:
            element.draw(screen, self)
        for key in self.buildElements:
            self.buildElements[key].draw(screen, self)
        if (self.inBuildMode or self.inRobberMode):
            for selectElement in self.selectElements:
                selectElement.draw(screen, self)
        if (self.discardMode):
            for key in self.discardElements:
                self.discardElements[key].draw(screen, self)
        if (self.yearOfPlentyMode):
            for key in self.yearOfPlentyElements:
                self.yearOfPlentyElements[key].draw(screen, self)
        if (self.stealMode):
            for key in self.stealElements:
                self.stealElements[key].draw(screen, self)
        if (self.devCardMode):
            for key in self.devCardElements:
                self.devCardElements[key].draw(screen, self)
        self.drawCurrentPlayer(screen)
        self.drawResources(screen)
        self.drawDevCards(screen)
    
    # Draws the resource panel at the bottom of the screen
    def drawResources(self, screen):
        player = self.board.players[self.currentPlayer]
        x, y = windowConfig.RESOURCES
        width, height = windowConfig.RESOURCES_SIZE
        pygame.draw.rect(screen, Colors.WHITE, (x, y, width, height))
        pygame.draw.rect(screen, Colors.BLACK, (x, y, width, height), 1)
        if (not isinstance(player, AIPlayer) or not self.fogOfWar):
            resources = player.resources
        else:
            resources = {'lumber':'??', 'brick':'??', 'sheep':'??', 'grain':'??', 'ore':'??'}
        resourceText = f"{resources['lumber']} Lumber, {resources['brick']} Brick, {resources['sheep']} Sheep, {resources['grain']} Grain, {resources['ore']} Ore"
        resourceLabel = Text.RESOURCE_FONT.render(resourceText, True, Colors.BLACK)
        resourcePos = resourceLabel.get_rect()
        resourcePos.center = pygame.Rect(x, y, width, height).center
        screen.blit(resourceLabel, resourcePos)
    
    # Draws the development card counters
    def drawDevCards(self, screen):
        player = self.board.players[self.currentPlayer]
        x, y = windowConfig.DEVCARDS
        width, height = windowConfig.DEVCARDS_SIZE
        pygame.draw.rect(screen, Colors.WHITE, (x, y, width, height))
        pygame.draw.rect(screen, Colors.BLACK, (x, y, width, height), 1)
        if (not isinstance(player, AIPlayer) or not self.fogOfWar):
            devCards = player.devCards
        else:
            devCards = {'knight':'??', 'yearOfPlenty':'??', 'monopoly':'??', 'roadBuilding':'??'}
        devCardText = f"{devCards['knight']} Knight, {devCards['yearOfPlenty']} Year of Plenty" # {devCards['monopoly']} Monopoly, {devCards['roadBuilding']} Rd Bldg
        devCardLabel = Text.RESOURCE_FONT.render(devCardText, True, Colors.BLACK)
        devCardPos = devCardLabel.get_rect()
        devCardPos.center = pygame.Rect(x, y, width, height).center
        screen.blit(devCardLabel, devCardPos)

    # Draws the current player's on the screen
    def drawCurrentPlayer(self, screen):
        currentPlayer = self.currentPlayer + 1
        player = self.board.players[self.currentPlayer]
        playerType = 'COM Player' if isinstance(player, AIPlayer) else 'Player'
        if (self.discardMode):
            remaining = player.countCards() - player.discardGoal
            currentPlayerText = Text.CURRENT_PLAYER_FONT.render(f'{playerType} {currentPlayer} Must Discard {remaining} Cards!', True, Colors.RED_1)
        elif (self.inRobberMode):
            currentPlayerText = Text.CURRENT_PLAYER_FONT.render(f'{playerType} {currentPlayer} Must Move the Robber!', True, Colors.RED_1)
        elif (self.stealMode):
            currentPlayerText = Text.CURRENT_PLAYER_FONT.render(f'{playerType} {currentPlayer} May Steal!', True, Colors.RED_1)
        else:
            currentPlayerText = Text.CURRENT_PLAYER_FONT.render(f'{playerType} {currentPlayer}\'s Turn', True, Colors.BLACK)
        
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
                hexFill = Utils.getFill(tile)
                leftOffset = ((self.board.q - rowLen) / 2) * self.hexWidth + self.boardBounds[0]
                x0 = leftOffset + j * self.hexWidth
                x1 = leftOffset + (j + 1) * self.hexWidth
                y0 = i * self.ySpacing + self.boardBounds[1]
                y1 = y0 + self.hexHeight
                center = (int(x0 + (x1-x0)/2), int(y0 + (y1-y0)/2))
                hexPoints = CatanMath.getHexagonPoints((x0, y0, x1, y1))
                pygame.draw.polygon(screen, hexFill, hexPoints)
                if (tile.type != None):
                    tileType = tile.type
                else:
                    tileType = 'desert'
                hexImage = self.loadImageFromCache("resources/assets/images/" + tileType + ".png")
                hexImage = pygame.transform.scale(hexImage, (int(self.hexWidth), int(self.hexHeight)))
                hexPos = hexImage.get_rect()
                hexPos.center = ((x0 + (x1-x0)/2), (y0 + (y1-y0)/2))
                screen.blit(hexImage, hexPos)
                # self.drawPorts(screen, (i, j+firstIndex), hexPoints, center)
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
                roadArgs = CatanMath.getThickAALine(point1, point2, 5)
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
            color = Colors.WHITEISH
            if (number == active and not hasRobber):
                color = Colors.GOLD_1
            pygame.draw.circle(screen, color, center, tokenSize)
            gfxdraw.aacircle(screen, center[0], center[1], tokenSize, Colors.BLACK)
            if (number in [6, 8]):
                tokenColor = Colors.BLACK
            else:
                tokenColor = Colors.BLACK
            if (hasRobber):
                tokenColor = Colors.GRAY
            token = Text.TOKEN_FONT.render(str(number), True, tokenColor)
            tokenSurf = token.get_rect()
            tokenSurf.center = center
            screen.blit(token, tokenSurf)
        if (hasRobber):
            robberImage = pygame.image.load("resources/assets/images/robber.png")
            scaleFactor = windowConfig.ROBBER_SCALE
            robberImage = pygame.transform.scale(robberImage, (int(scaleFactor * self.hexWidth), int(scaleFactor * self.hexHeight)))
            robberPos = robberImage.get_rect()
            robberPos.centerx = center[0]
            robberPos.centery = center[1] + 0.3 * hexHeight
            screen.blit(robberImage, robberPos)
    
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
                gfxdraw.aapolygon(screen, triangle, Colors.GOLD_DISABLED)
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
    
CatanGame(width=windowConfig.WIDTH, height=windowConfig.HEIGHT, title='Catan: The Settlers of Python').run()