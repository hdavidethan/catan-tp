#########################################################################
# AIPlayer File
# Contains the AIPlayer subclass of Player; creates and controls the AI
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

import random, copy
from resources.game.player import Player
from config.colors import Colors
from resources.game.utils import Utils
from resources.gui.button import Button
from resources.game.axial import *

class AIPlayer(Player):
    def __init__(self, index):
        super().__init__(index)
        print(f'Initialized AI Player {self.index}')

    def startTurn(self, game):
        moves = self.getLegalMoves(game)
        if (len(moves) > 0):
            nextMove = random.choice(moves)
            self.doMove(game, nextMove)
    
    def startDiscard(self, game):
        while not game.checkEndTurnConditions(self):
            resources = game.checkDiscardConditions(self)
            nextDiscard = random.choice(resources)
            Button.discardHandler(game, ('discard', nextDiscard))

    def doMove(self, game, listOfMoves):
        move, validSet = listOfMoves
        if (move == 'setup'):
            nodeIndex = self.chooseBestNode(game)
            firstNode = game.board.nodes[nodeIndex]
            Button.buildModeHandler(game, ('buildConfirm', (firstNode, self)))
            roadIDs = list(firstNode.getRoads(game.board))
            roads = []
            for roadID in roadIDs:
                roads.append(game.board.edges[roadID])
            self.doRoadMove(game, roads)
            
        elif (move == 'buildRoad'):
            if (len(validSet) > 1):
                self.doRoadMove(game, validSet)

    def doRoadMove(self, game, roads):
        nextRoad = None
        found = False
        paths = copy.deepcopy(self.chooseBestRoad(game))
        while not found:
            if (len(paths) == 0):
                found = None
                break
            shortestPath = min(paths, key=len)
            firstNode = game.board.nodes[shortestPath[0]]
            nextNode = game.board.nodes[shortestPath[1]]
            nextRoad = firstNode.getRoadBetweenNodes(nextNode, game.board)
            if (nextRoad in roads):
                found = True
            else:
                paths.remove(shortestPath)
        if (found == None):
            nextRoad = random.choice(list(roads))
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
        if (settlement[1]):
            validSettlements = self.getLegalSettlements(game)
            return []
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
    
    def getLegalSettlements(self, game):
        pass

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
    
    def chooseBestRoad(self, game):
        tileOrder = self.chooseClosestTile(game)
        minimumDistance = -1
        minimumTile = None
        destination = game.board.nodes[self.chooseBestNode(game)]
        paths = []
        for tile in tileOrder:
            for node in tile.nodes:
                if (node.owner == self):
                    nodeOrder = self.dijkstraRoads(game, node, destination)
                    paths.append(nodeOrder)
        return paths
    
    def dijkstraRoads(self, game, start, dest):
        inf = float('inf')
        distances = {node.id: inf for node in game.board.nodes}
        distances[start.id] = 0
        bestDistance, bestPath = self.recursiveDijkstra(game, start, dest, distances, [start.id])
        return bestPath

    def recursiveDijkstra(self, game, start, dest, distances, path):
        adjacentNodes = start.getAdjacentNodes(game.board)
        bestDistance = distances[dest.id]
        bestPath = path
        for node in adjacentNodes:
            road = node.getRoadBetweenNodes(start, game.board)
            if (road.road == None):
                if (1+distances[start.id] < distances[node.id]):
                    distances[node.id] = 1+distances[start.id]
                    tmpDistance, tmpPath = self.recursiveDijkstra(game, node, dest, distances, path+[node.id])
                    if (tmpDistance < bestDistance):
                        bestDistance = tmpDistance
                        bestPath = tmpPath
        return bestDistance, bestPath

    def chooseSourceRoad(self, game, node):
        result = []
        startRoads = node.getRoads(game.board)
        for startRoad in startRoads:
            if (startRoad.road == None):
                result.append(startRoad)
        return result

    def chooseClosestTile(self, game):
        board = game.board
        ownedTiles = set()
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen):
                tile = board.hexBoard[i][j+firstIndex]
                for node in tile.nodes:
                    if node.owner == self:
                        ownedTiles.add(tile)
        if (ownedTiles != set()):
            result = []
            tmp = copy.copy(list(ownedTiles))
            while len(tmp) > 0:
                minTile = self.findMinimumDistance(game, tmp)
                tmp.remove(minTile)
                result.append(minTile)
        return result
    
    def findMinimumDistance(self, game, tiles):
        bestNode = game.board.nodes[self.chooseBestNode(game)]
        possibleTiles = self.findTilesFromNode(game, bestNode)
        minDistance = -1
        minTile = None
        for tile in possibleTiles:
            for ownedTile in tiles:
                ownedR, ownedQ = ownedTile.pos
                checkR, checkQ = tile.pos
                distance = axialDistance(ownedR, ownedQ, checkR, checkQ)
                if (distance < minDistance or minDistance == -1):
                    minDistance = distance
                    minTile = ownedTile
        return minTile
        
    def findTilesFromNode(self, game, node):
        board = game.board
        found = set()
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen):
                tile = board.hexBoard[i][j+firstIndex]
                for checkedNode in tile.nodes:
                    if checkedNode == node:
                        found.add(tile)
        return found
        
