import random
from resources.game.player import Player
from config.colors import Colors
from resources.game.utils import Utils
from resources.gui.button import Button

class AIPlayer(Player):
    def __init__(self, index):
        super().__init__(index)
        print(f'Initialized AI Player {self.index}')
    
    def startTurn(self, game):
        self.getLegalMoves(game)
    
    def getLegalMoves(self, game):
        # Check Build
        road, settlement, city, devCard = game.checkBuildConditions(self)
        if (game.setupMode):
            nodeIndex = self.chooseBestNode(game)
            firstNode = game.board.nodes[nodeIndex]
            Button.buildModeHandler(game, ('buildConfirm', (firstNode, game.board.players[game.currentPlayer])))
            roads = list(firstNode.getRoads(game.board))
            roadIndex = random.choice(roads)
            firstRoad = game.board.edges[roadIndex]
            Button.buildModeHandler(game, ('buildConfirm', (firstRoad, game.board.players[game.currentPlayer])))


    def chooseBestNode(self, game):
        nodeList = []
        for node in game.board.nodes:
            if (node.owner == None and node.buildable):
                nodeList.append(node.getNodeValue(game.board))
            else:
                nodeList.append((0, []))
        maxIndex = -1
        maxValue = -1
        for i in range(len(nodeList)):
            value, numList = nodeList[i]
            if (maxIndex == -1):
                maxValue = value
                maxIndex = i
            elif (value > maxValue):
                maxValue = value
                maxIndex = i
        return maxIndex
