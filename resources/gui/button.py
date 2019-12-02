#########################################################################
# Button File
# Contains the Button subclass of Element; creates buttons
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

from resources.gui.element import Element
from resources.gui.roundedRect import drawRoundedRect
from resources.game.node import Node
from resources.game.edge import Edge
from resources.game.utils import Utils
from config.colors import Colors
from config.text import Text
import pygame

class Button(Element):
    def __init__(self, pos, size, text, colors, binding, radius=0, isDisabled=False, font=Text.BUTTON_FONT):
        super().__init__(pos, size)
        self.text = text
        self.radius = radius
        self.binding = binding
        self.colors = colors
        self.isDisabled = isDisabled
        self.font = font
    
    def __eq__(self, other):
        return isinstance(other, Button) and (self.pos == other.pos)
    
    def __hash__(self):
        return hash((self.pos, self.size, self.text))

    def getColor(self, rectArgs, game):
        mx, my = pygame.mouse.get_pos()
        x0, y0, width, height = rectArgs
        x1, y1 = x0 + width, y0 + height
        primary, secondary, text, buttonDisabled, textDisabled = self.colors
        if (self.isDisabled):
            return (buttonDisabled, textDisabled)
        else:
            if (mx > x0 and mx < x1 and my > y0 and my < y1 and not game.isPaused):
                return (secondary, text)
            else:
                return (primary, text)
    
    # Handler for onClick events.
    def onClick(self, game):
        if (not self.isDisabled):
            if (isinstance(self.binding, tuple)):
                if (self.binding[0] == 'changeMode'):
                    if ('AI' in self.binding):
                        game.setActiveMode(self.binding[1], AIGame=True)
                    else:
                        game.setActiveMode(self.binding[1])
                elif (self.binding[0] == 'endTurn'):
                    if (game.discardMode):
                        game.endDiscard()
                    elif (game.yearOfPlentyMode):
                        game.endYearOfPlenty()
                    else:
                        game.endTurn()
                elif (self.binding[0] == 'build'):
                    game.buildMode(self.binding[1])
                elif (self.binding[0] == 'buildConfirm'):
                    Button.buildModeHandler(game, self.binding)
                elif (self.binding[0] == 'discard'):
                    Button.discardHandler(game, self.binding)
                elif (self.binding[0] == 'claim'):
                    Button.claimHandler(game, self.binding)
                elif (self.binding[0] == 'placeRobber'):
                    game.inRobberMode = False
                    tile = self.binding[1][0]
                    oldR, oldQ = game.oldRobberPos
                    game.board.hexBoard[oldR][oldQ].hasRobber = False
                    tile.hasRobber = True
                    game.stealChoice(self.binding[1])
                elif (self.binding[0] == 'stealConfirm'):
                    currentPlayer = game.board.players[game.currentPlayer]
                    victim = self.binding[1]
                    resource = Utils.stealRandomResource(victim)
                    victim.resources[resource] -= 1
                    currentPlayer.resources[resource] += 1
                    game.stealMode = False
                    game.checkEndTurnConditions(currentPlayer)
                elif (self.binding[0] == 'devCard'):
                    game.startDevCard()
                elif (self.binding[0] == 'confirmDevCard'):
                    Button.devCardHandler(game, self.binding)
                elif (self.binding[0] == 'quit'):
                    game._running = False
    
    def draw(self, screen, game):
        rectArgs = self.getRectArgs()
        bgColor, textColor = self.getColor(rectArgs, game)
        if (self.radius == 0):
            pygame.draw.rect(screen, bgColor, rectArgs)
        else:
            drawRoundedRect(screen, rectArgs, bgColor, self.radius)
        if (self.text != None):
            text = self.font.render(self.text, True, textColor)
            textSurf = text.get_rect()
            textSurf.center = self.pos
            screen.blit(text, textSurf)
    
    @staticmethod
    def buildModeHandler(game, binding):
        buildObject, player = binding[1]
        if (isinstance(buildObject, Node)):
            buildObject.nodeLevel += 1
            if (buildObject.nodeLevel == 1):
                if (not game.setupMode):
                    player.resources['lumber'] -= 1
                    player.resources['sheep'] -= 1
                    player.resources['brick'] -= 1
                    player.resources['grain'] -= 1
                elif (game.turn // 4 == 0):
                    buildObject.setupCollect(player, game.board)
                player.settlements.add(buildObject.id)
                buildObject.checkAdjacencies(game.board)
            elif (buildObject.nodeLevel == 2):
                player.resources['ore'] -= 3
                player.resources['grain'] -= 2
                player.settlements.remove(buildObject.id)
                player.cities.add(buildObject.id)
            buildObject.owner = player
        elif (isinstance(buildObject, Edge)):
            if (not game.setupMode):
                player.resources['lumber'] -= 1
                player.resources['brick'] -= 1
            player.roads.add(buildObject.id)
            buildObject.road = player.bgColor
        game.inBuildMode = False
        game.checkBuildConditions(player)
        player.longestRoad = player.countRoads(game)
        game.checkVictoryPoints()

    @staticmethod
    def devCardHandler(game, binding):
        game.devCardMode = False
        devCard, player = binding[1]
        if (devCard == 'knight'):
            game.robberMode()
            player.devCards['knight'] -= 1
            player.largestArmy += 1
        elif (devCard == 'yearOfPlenty'):
            game.startYearOfPlenty()
            player.devCards['yearOfPlenty'] -= 1
    
    @staticmethod
    def discardHandler(game, binding):
        player = game.board.players[game.currentPlayer]
        game.discardResource(player, binding[1])
    
    @staticmethod
    def claimHandler(game, binding):
        player = game.board.players[game.currentPlayer]
        game.claimResource(player, binding[1])