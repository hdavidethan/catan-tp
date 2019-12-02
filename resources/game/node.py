#########################################################################
# Node File
# Creates and handles the Nodes on the Catan board
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

import copy
from resources.game.utils import Utils

class Node(object):
    def __init__(self, id, port=None):
        self.id = id
        self.port = port
        self.pos = None
        self.owner = None
        self.nodeLevel = 0 # 1 and 2 for settlement and city
        self.buildable = True

    def __repr__(self):
        port = f'with Port {self.port}' if self.port != None else 'without a port' 
        return f'<Node at id [{self.id}], {port}>'
    
    def __eq__(self, other):
        return isinstance(other, Node) and other.id == self.id
    
    def __hash__(self):
        return hash((self.id,))
    
    def checkAdjacencies(self, board):
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = board.hexBoard[i][j+firstIndex]
                if self in tile.nodes:
                    nodeIndex = tile.nodes.index(self)
                    node1 = tile.nodes[nodeIndex-1]
                    node2 = tile.nodes[(nodeIndex+1)%6]
                    board.nodes[node1.id].buildable = False
                    board.nodes[node2.id].buildable = False
    
    def getRoads(self, board):
        seen = set()
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen):
                tile = board.hexBoard[i][j+firstIndex]
                if self in tile.nodes:
                    nodeIndex = tile.nodes.index(self)
                    road1 = board.edges[tile.edges[nodeIndex].id]
                    road2 = board.edges[tile.edges[(nodeIndex-1)%6].id]
                    if (road1 not in seen):
                        seen.add(road1.id)
                    if (road2 not in seen):
                        seen.add(road2.id)
        return seen
    
    def setupCollect(self, player, board):
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = board.hexBoard[i][j+firstIndex]
                if self in tile.nodes:
                    resource = Utils.getResourceFromType(tile.type)
                    if (resource != None):
                        player.resources[resource] += self.nodeLevel
    
    def getNodeValue(self, board):
        resList = []
        res = 0
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = board.hexBoard[i][j+firstIndex]
                if self in tile.nodes and tile.number != None:
                    res += Utils.getProbabilityFromNumber(tile.number)
                    resList.append((tile.number, Utils.getProbabilityFromNumber(tile.number)))
        return res, resList
    
    def collectFromNumber(self, player, n, board):
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = board.hexBoard[i][j+firstIndex]
                if self in tile.nodes:
                    resource = Utils.getResourceFromType(tile.type)
                    if (tile.number == n):
                        player.resources[resource] += self.nodeLevel
    
    def checkOwnedRoads(self, board, player):
        indexes = self.getRoads(board)
        roads = set()
        for index in indexes:
            roads.add(board.edges[index])
        for edge in roads:
            if (edge.road == player.bgColor):
                return True

    def getAdjacentNodes(self, board):
        seen = set()
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = board.hexBoard[i][j+firstIndex]
                if self in tile.nodes:
                    nodeIndex = tile.nodes.index(self)
                    node1 = tile.nodes[nodeIndex-1]
                    node2 = tile.nodes[(nodeIndex+1)%6]
                    if (node1 not in seen):
                        seen.add(node1)
                    if (node2 not in seen):
                        seen.add(node2)
        return seen
    
    def getRoadBetweenNodes(self, other, board):
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = board.hexBoard[i][j+firstIndex]
                if self in tile.nodes and other in tile.nodes:
                    if (tile.nodes.index(self) - tile.nodes.index(other) > 0 or
                        tile.nodes.index(self) == 0 and tile.nodes.index(other) == 5):
                        edgeIndex = tile.nodes.index(other)
                    elif (tile.nodes.index(other) - tile.nodes.index(self) > 0 or
                        tile.nodes.index(other) == 0 and tile.nodes.index(self) == 5):
                        edgeIndex = tile.nodes.index(self)
                    else:
                        return None
                    return board.edges[tile.edges[edgeIndex].id]