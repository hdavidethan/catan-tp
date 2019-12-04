#########################################################################
# Board File
# Contains Board class; stores and creates the entire Catan board
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

from resources.game.axial import *
from resources.game.node import Node
from resources.game.tile import Tile
from resources.game.edge import Edge
from resources.game.player import Player
from resources.game.aiplayer import AIPlayer
import copy, random

class Board(object):
    def __init__(self, r=5, q=5, human=4, ai=0):
        self.r = r
        self.q = q
        self.hexBoard = generateAxialList(self.r, self.q)
        self.hexCount = hexCount(self.r, self.q)

        self.edges = []
        self.generateEdges()
        self.assignEdges()

        self.nodes = []
        self.ports = []
        self.generateNodes()
        self.assignNodes()

        self.assignTypes()
        self.assignNumbers()

        self.humanCount = human
        self.aiCount = ai
        self.players = []
        playerIndex = 0
        for i in range(self.humanCount):
            self.players.append(Player(playerIndex))
            playerIndex += 1
        for i in range(self.aiCount):
            self.players.append(AIPlayer(playerIndex))
            playerIndex += 1
    
    # Generates the Edge objects into a list.
    def generateEdges(self):
        r, q = sideCount(self.r, self.q)
        boardEdges = (q * 2) * 2 + ((r * 2 - 1) + (r * 2 - 2)) * 2
        edgesPerHex = 6
        uniqueHexCount = (boardEdges + self.hexCount * edgesPerHex) // 2
        for i in range(uniqueHexCount):
            self.edges.append(Edge(i))
    
    # Assigns each object in edge list to a tile.
    def assignEdges(self):
        edgeCounter = 0
        tmpBoard = copy.deepcopy(self.hexBoard)
        for row in range(len(self.hexBoard)):
            for col in range(len(self.hexBoard[0])):
                if (self.hexBoard[row][col] != None):
                    tile = tmpBoard[row][col]
                    createdDirs = [0, 1, 5] # Directions that probably exist
                    for i in range(6):
                        adj = getAdjacencyInDirection((row, col), i)
                        # Copies Edge object for adjacent sides.
                        if (i in createdDirs and adj != None):
                            adjRow, adjCol = adj[0]
                            toAdd = tmpBoard[adjRow][adjCol].edges[adj[1]]
                            tile.edges.append(toAdd)
                        # Assigns new edges
                        else:
                            toAdd = self.edges[edgeCounter]
                            tile.edges.append(toAdd)
                            edgeCounter += 1
        self.hexBoard = tmpBoard

    # Generate the nodes for assignment
    def generateNodes(self):
        # Nodes with ports:
        ports = {2:1, 6:1, 10:2, 11:2, 22:3, 23:3, 37:4, 45:4, 52:5, 53:5, 47:6,
                51:6, 39:7, 40:7, 25:8, 28:8, 5:9, 14:9}
        portTypes = ['wildcard'] * 4 + ['lumber', 'sheep', 'grain', 'brick', 'ore']
        random.shuffle(portTypes)
        self.ports = copy.copy(portTypes)
        totalNodes = 54
        for i in range(totalNodes):
            if (i in ports):
                self.nodes.append(Node(i, ports[i]))
            else:
                self.nodes.append(Node(i))

    # Assign the nodes to the board (TEMPORARY!!)
    def assignNodes(self):
        assignment = [[0,1,2,3,4,5],[2,6,7,8,9,3],[7,10,11,12,13,8],
                      [14,5,4,15,16,17],[4,3,9,18,19,15],[9,8,13,20,21,18],[13,12,22,23,24,20],
                      [25,17,16,26,27,28],[16,15,19,29,30,26],[19,18,21,31,32,29],[21,20,24,33,34,31],[24,23,35,36,37,33],
                      [27,26,30,38,39,40],[30,29,32,41,42,38],[32,31,34,43,44,41],[34,33,37,45,46,43],
                      [39,38,42,47,48,49],[42,41,44,50,51,47],[44,43,46,52,53,50]]
        tileCounter = 0
        tmpBoard = copy.deepcopy(self.hexBoard)
        for row in range(len(self.hexBoard)):
            for col in range(len(self.hexBoard[0])):
                if (self.hexBoard[row][col] != None):
                    tile = tmpBoard[row][col]
                    for i in assignment[tileCounter]:
                        tile.nodes.append(self.nodes[i])
                    tileCounter += 1
        self.hexBoard = tmpBoard

    # Assign types to each Tile on the board
    def assignTypes(self):
        resources = (['desert'] + ['hills'] * 3 + ['forest'] * 4 +
                    ['mountains'] * 3 + ['pasture'] * 4 + ['fields'] * 4)
        random.shuffle(resources)
        for row in range(len(self.hexBoard)):
            for col in range(len(self.hexBoard[0])):
                if (self.hexBoard[row][col] != None):
                    self.hexBoard[row][col].type = resources.pop()
                    if (self.hexBoard[row][col].type == 'desert'):
                        self.hexBoard[row][col].hasRobber = True

    # Assign number tokens to each Tile on the board
    def assignNumbers(self):
        # Default Catan order with first as last index (reversed)
        number = [11, 3, 6, 5, 4, 9, 10, 8, 4, 11, 12, 9, 10, 8, 3, 6, 2, 5]
        # Order is constant
        order = [(0, 2), (1, 1), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2),
                (3, 3), (2, 4), (1, 4), (0, 4), (0, 3), (1, 2), (2, 1), (3, 1),
                (3, 2), (2, 3), (1, 3), (2, 2)]
        for r, q in order:
            if (self.hexBoard[r][q].type != 'desert'):
                self.hexBoard[r][q].number = number.pop()
