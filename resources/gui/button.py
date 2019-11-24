from resources.gui.element import Element
from resources.gui.roundedRect import drawRoundedRect
from resources.game.node import Node
from resources.game.edge import Edge
from config.colors import Colors
from config.text import Text
import pygame

# Valid Bindings: changeMode, quit, pause

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

    def getColor(self, rectArgs):
        mx, my = pygame.mouse.get_pos()
        x0, y0, width, height = rectArgs
        x1, y1 = x0 + width, y0 + height
        primary, secondary, text, buttonDisabled, textDisabled = self.colors
        if (self.isDisabled):
            return (buttonDisabled, textDisabled)
        else:
            if (mx > x0 and mx < x1 and my > y0 and my < y1):
                return (secondary, text)
            else:
                return (primary, text)
    
    # Handler for onClick events.
    def onClick(self, game):
        if (not self.isDisabled):
            if (isinstance(self.binding, tuple)):
                if (self.binding[0] == 'changeMode'):
                    game.setActiveMode(self.binding[1])
                elif (self.binding[0] == 'endTurn'):
                    game.endTurn()
                elif (self.binding[0] == 'build'):
                    game.buildMode(self.binding[1])
                elif (self.binding[0] == 'buildConfirm'):
                    buildObject, player = self.binding[1]
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
                    game.checkVictoryPoints()
                elif (self.binding[0] == 'quit'):
                    game._running = False
    
    def draw(self, screen):
        rectArgs = self.getRectArgs()
        bgColor, textColor = self.getColor(rectArgs)
        if (self.radius == 0):
            pygame.draw.rect(screen, bgColor, rectArgs)
        else:
            drawRoundedRect(screen, rectArgs, bgColor, self.radius)
        if (self.text != None):
            text = self.font.render(self.text, True, textColor)
            textSurf = text.get_rect()
            textSurf.center = self.pos
            screen.blit(text, textSurf)