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
        self.priorityNode = None

    # Starts the turn for AI Players (analogous to startTurn() in app.py)
    def startTurn(self, game):
        playerIndex = self.index + 1
        moves = self.getLegalMoves(game)
        if (len(moves) > 0):
            actions = []
            moveDict = dict()
            nextMove = [None, set()]
            for move in moves:
                action, moveSet = move
                actions.append(action)
                moveDict[action] = move
            if (self.reachedPriorityNode(game)):
                tmpDict = copy.deepcopy(moveDict)
                for key in tmpDict:
                    if (key not in ['buildSettlement', 'buildCity']):
                        del moveDict[key]
            if ('buildSettlement' in actions and moveDict['buildSettlement'][1] != set()):
                nextMove = moveDict['buildSettlement']
            elif (len(moveDict.keys()) > 0):
                actions = []
                for key in moveDict:
                    actions.append(key)
                if ('setup' in actions):
                    nextAction = 'setup'
                elif ('buildRoad' in actions):
                    nextAction = 'buildRoad'
                elif ('buildCity' in actions):
                    nextAction = 'buildCity'
                elif ('buildDevCard' in actions):
                    nextAction = 'buildDevCard'
                nextMove = moveDict[nextAction]
            self.doMove(game, nextMove)
    
    # Checks if the AI Player has a road connected to the priority node.
    def reachedPriorityNode(self, game):
        if (not game.setupMode):
            priorityNode = game.board.nodes[self.priorityNode]
            roadIDs = priorityNode.getRoads(game.board)
            roads = {game.board.edges[roadID] for roadID in roadIDs}
            roadOwners = [road.road for road in roads]
            return self.bgColor in roadOwners
        return False

    # Starts the Discard Phase for AI Players (analogous to startDiscard() in app.py)
    def startDiscard(self, game):
        while not game.checkEndTurnConditions(self):
            resources = game.checkDiscardConditions(self)
            nextDiscard = random.choice(resources)
            Button.discardHandler(game, ('discard', nextDiscard))

    # Starts the Robber Place Mode for AI Players (analogous to method in app.py)
    def robberMode(self, game, tileSet):
        board = game.board
        tileValues = dict()
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = board.hexBoard[i][j+firstIndex]
                r, q = i, j + firstIndex
                value = 0
                for node in tile.nodes:
                    if (node.owner != None and node.owner != self):
                        value += 1
                    elif (node.owner == self):
                        value -= 1
                tileValues[(i,j)] = value
        for r, q in tileValues:
            if (Tile(r, q) not in tileSet):
                tileValues[(r, q)] = -float('inf')
        values = list(tileValues.values())
        keys = list(tileValues.keys())
        maxTile = keys[values.index(max(values))]
        for tile in tileSet:
            if (tile.pos == maxTile):
                Button.robberHandler(game, ('placeRobber', (tile, self)))
                break
    
    # Starts the Steal Mode for AI Players (analogoes to method in app.py)
    def stealChoice(self, game, victimSet):
        choice = game.board.players[random.choice(list(victimSet))]
        Button.stealHandler(game, ('stealConfirm', choice))

    # Does the given move
    def doMove(self, game, listOfMoves):
        self.getBestNodeList(game)
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
        
        elif (move == 'buildCity'):
            if (len(validSet) >= 1):
                self.doCityMove(game, validSet)

        elif (move == 'buildSettlement'):
            if (len(validSet) >= 1):
                self.doSettlementMove(game, validSet)

        elif (move == 'buildRoad'):
            if (len(validSet) >= 1):
                self.doRoadMove(game, validSet)
        
        elif (move == 'buildDevCard'):
            game.buildMode('devCard')
    
    # Performs the move if the move is a road move.
    def doRoadMove(self, game, roads):
        nextRoad = None
        found = False
        paths = copy.deepcopy(self.chooseBestRoad(game))
        while not found:
            if (len(paths) == 0):
                found = None
                break
            shortestPath = min(paths, key=len)
            while len(shortestPath) < 2:
                paths.remove(shortestPath)
                if (len(paths) > 0):
                    shortestPath = min(paths, key=len)
                else:
                    return
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
    
    # Performs the move if the move is a settlement move.
    def doSettlementMove(self, game, settlements):
        nextSettlement = None
        maxValue = -1
        for settlement in settlements:
            value = settlement.getNodeValue(game.board)[0]
            if (value > maxValue or maxValue == -1):
                nextSettlement = settlement
                maxValue = value
        Button.buildModeHandler(game, ('buildConfirm', (nextSettlement, self)))

    # Performs the move if the move is a city move.
    def doCityMove(self, game, cities):
        nextCity = random.choice(list(cities))
        Button.buildModeHandler(game, ('buildConfirm', (nextCity, self)))

    # Returns the legal moves for the player
    def getLegalMoves(self, game):
        # Check if setup
        if (game.setupMode):
            return [('setup', None)]
        # Check Build
        else:
            self.setPriorityNode(game)
            road, settlement, city, devCard = game.checkBuildConditions(self)
            moves = []
            if (road[1]):
                validRoads = self.getLegalRoads(game)
                moves.append(('buildRoad', validRoads))
            if (settlement[1]):
                validSettlements = self.getLegalSettlements(game)
                moves.append(('buildSettlement', validSettlements))
            if (city[1]):
                validCities = self.getLegalCities(game)
                moves.append(('buildCity', validCities))
            if (devCard[1]):
                moves.append(('buildDevCard', None))
            return moves

    # Returns the legal roads to build
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
    
    # Returns the legal settlements to build
    def getLegalSettlements(self, game):
        seen = set()
        for node in game.board.nodes:
            validNode = node.checkOwnedRoads(game.board, self)
            if (node.nodeLevel == 0 and node.buildable and validNode):
                seen.add(node)
        return seen
    
    # Returns the legal cities to build
    def getLegalCities(self, game):
        seen = set()
        for node in game.board.nodes:
            if (node.nodeLevel == 1 and node.owner.index == self.index):
                seen.add(node)
        return seen

    # Chooses the node with highest value.
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

    # Sets the priority node for AI Players
    def setPriorityNode(self, game):
        if (self.priorityNode == None):
            nodeList = self.getBestNodeList(game)
            validNodes = []
            for nodeTuple in nodeList:
                value, numList, nodeID = nodeTuple
                node = game.board.nodes[nodeID]
                bestDistance = -1
                bestStart = None
                for ownedNodeID in self.getOwnedNodes():
                    ownedNode = game.board.nodes[ownedNodeID]
                    path, distance = self.dijkstraRoads(game, ownedNode, node)
                    if (distance < bestDistance or bestDistance == -1):
                        bestDistance = distance
                        bestStart = ownedNode
                if (bestDistance < 4 and node.buildable):
                    validNodes.append(node.id)
            self.priorityNode = random.choice(validNodes)
        elif (not game.board.nodes[self.priorityNode].buildable or game.board.nodes[self.priorityNode].owner != None):
            self.priorityNode = None
            self.setPriorityNode(game)
    
    # Returns a list of best nodes in descending order
    def getBestNodeList(self, game):
        nodeList = []
        for node in game.board.nodes:
            if (node.owner == None and node.buildable):
                value, numList = node.getNodeValue(game.board)
                nodeList.append((value, numList, node.id))
            else:
                nodeList.append((0, [], node.id))
        nodeList.sort(reverse=True)
        return nodeList

    # Chooses the best possible road given the shortest path
    def chooseBestRoad(self, game):
        if (game.setupMode):
            destination = game.board.nodes[self.chooseBestNode(game)]
        else:
            destination = game.board.nodes[self.priorityNode]
        tileOrder = self.chooseClosestTile(game, destination)
        minimumDistance = -1
        minimumTile = None
        paths = []
        for tile in tileOrder:
            for node in tile.nodes:
                roadIDs = node.getRoads(game.board)
                roads = {game.board.edges[roadID] for roadID in roadIDs}
                roadOwners = [road.road for road in roads]
                noOwnerCondition = node.owner == None and (None in roadOwners and self.bgColor in roadOwners)
                if (node.owner == self or noOwnerCondition):
                    nodeOrder = self.dijkstraRoads(game, node, destination)[0]
                    paths.append(nodeOrder)
        return paths

    # Wrapper function for shortest path (recursiveDijkstra)
    def dijkstraRoads(self, game, start, dest):
        inf = float('inf')
        distances = {node.id: inf for node in game.board.nodes}
        distances[start.id] = 0
        bestDistance, bestPath = self.recursiveDijkstra(game, start, dest, distances, [start.id])
        return bestPath, bestDistance

    # Recursive function to get shortest path
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

    # Chooses the ideal source road to build from.
    def chooseSourceRoad(self, game, node):
        result = []
        startRoads = node.getRoads(game.board)
        for startRoad in startRoads:
            if (startRoad.road == None):
                result.append(startRoad)
        return result

    # Chooses the closest tile to a given node
    def chooseClosestTile(self, game, node):
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
                minTile = self.findMinimumDistance(game, tmp, node)
                tmp.remove(minTile)
                result.append(minTile)
        return result
    
    # Find the minimum distance to a given tile from another tile
    def findMinimumDistance(self, game, tiles, node):
        possibleTiles = self.findTilesFromNode(game, node)
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
    
    # Find the tiles surrounding a node
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
        
