import random, copy
from resources.game.player import Player
from config.colors import Colors
from resources.game.utils import Utils
from resources.gui.button import Button

class AIPlayer(Player):
    def __init__(self, index):
        super().__init__(index)
        print(f'Initialized AI Player {self.index}')

    def startTurn(self, game):
        moves = self.getLegalMoves(game)
        if (len(moves) > 0):
            nextMove = random.choice(moves)
            self.doMove(game, nextMove)

    def doMove(self, game, listOfMoves):
        move, validSet = listOfMoves
        if (move == 'setup'):
            nodeIndex = self.chooseBestNode(game)
            firstNode = game.board.nodes[nodeIndex]
            Button.buildModeHandler(game, ('buildConfirm', (firstNode, self)))
            roads = list(firstNode.getRoads(game.board))
            roadIndex = random.choice(roads)
            firstRoad = game.board.edges[roadIndex]
            Button.buildModeHandler(game, ('buildConfirm', (firstRoad, self)))
        elif (move == 'buildRoad'):
            if (len(validSet) > 1):
                nextRoad = random.choice(list(validSet))
                Button.buildModeHandler(game, ('buildConfirm', (nextRoad, self)))

    def getLegalMoves(self, game):
        # Check if setup
        if (game.setupMode):
            return [('setup', None)]
        # Check Build
        road, settlement, city, devCard = game.checkBuildConditions(self)
        if (road[1]):
            validRoads = self.getLegalRoads(game)
            return [('buildRoad', validRoads)]
        else:
            return []

    def getLegalRoads(self, game):
        seen = set()
        for node in game.board.nodes:
            if (node.owner != None and node.owner.index == game.currentPlayer):
                roads = node.getRoads(game.board)
                for i in roads:
                    seen.add(game.board.edges[i])
            else:
                roads = node.getRoads(game.board)
                tmp = copy.copy(roads)
                found = False
                for i in roads:
                    if (game.board.edges[i].road == self.bgColor):
                        found = True
                        tmp.remove(i)
                if (found == True):
                    for i in tmp:
                        seen.add(game.board.edges[i])
        return seen
        

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
