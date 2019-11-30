#########################################################################
# Edge File
# Contains and handles Edges on the Catan Board
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

import copy

class Edge(object):
    def __init__(self, id):
        self.road = None
        self.id = id
        self.pos = None
    
    def __repr__(self):
        return f'<Edge at id [{self.id}]>'
    
    def __eq__(self, other):
        return isinstance(other, Edge) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
    
    def checkAdjacent(self, other, board):
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = board.hexBoard[i][j+firstIndex]
                if (self in tile.edges and other in tile.edges):
                    selfIndex = tile.edges.index(self)
                    otherIndex = tile.edges.index(other)
                    if (abs(selfIndex - otherIndex) == 1):
                        return True, tile
        return False, None
    
    def getRoads(self, board):
        for i in range(board.q):
            row = copy.copy(board.hexBoard[i])
            colCtr = 0
            while None in row:
                row.remove(None)
            firstIndex = board.hexBoard[i].index(row[0])
            rowLen = len(row)
            for j in range(rowLen): 
                tile = board.hexBoard[i][j+firstIndex]
                if (self in tile.edges):
                    index1 = tile.edges.index(self)
                    index2 = check1 + 1
                    node1 = tile.nodes[index1]
                    node2 = tile.nodes[index2]
                    roads1 = node1.getRoads(board)
                    roads1.remove(self)
                    roads2 = node2.getRoads(board)
                    roads2.remove(self)
                    return roads1, roads2