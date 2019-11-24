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

