from axial import *
import copy, random

class Board(object):
    def __init__(self, r=5, q=5):
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

    def assignNodes(self):
        nodeCounter = 0
        tmpBoard = copy.deepcopy(self.hexBoard)
        for row in range(len(self.hexBoard)):
            for col in range(len(self.hexBoard[0])):
                if (self.hexBoard[row][col] != None):
                    tile = tmpBoard[row][col]
                    createdDirs = [0, 1, 2, 5] # Directions that probably exist
                    while len(tile.nodes) < 6:
                        i = len(tile.nodes)
                        check = getAdjacencyInDirection((row, col), i)
                        if (check == None):
                            adj = getAdjacencyInDirection((row, col), (i-1)%6)
                            adjNodes = getNodeInDirection((row, col), (i-1)%6)
                        elif (i != 5):
                            adj = getAdjacencyInDirection((row, col), (i-1)%6)
                            adjRow, adjCol = adj[0]
                            checkLength = len(tmpBoard[adjRow][adjCol].nodes)
                            if (checkLength == 0):
                                adjNodes = getNodeInDirection((row, col), (i-1)%6)
                            else:
                                adj = getAdjacencyInDirection((row, col), i)
                                adjNodes = getNodeInDirection((row, col), i)
                        else:
                            adj = getAdjacencyInDirection((row, col), i)
                            adjNodes = (5, 3)
                        # Copies Edge object for adjacent sides.
                        if (i in createdDirs and adjNodes != None and adj != None):
                            adjRow, adjCol = adj[0]
                            node = adjNodes[1]
                            if (len(tmpBoard[adjRow][adjCol].nodes) != 0):
                                toAdd = tmpBoard[adjRow][adjCol].nodes[node]
                                tile.nodes.append(toAdd)
                            else:
                                toAdd = self.nodes[nodeCounter]
                                tile.nodes.append(toAdd)
                                nodeCounter += 1
                        # Assigns new edges
                        else:
                            toAdd = self.nodes[nodeCounter]
                            tile.nodes.append(toAdd)
                            nodeCounter += 1
                    print((row,col),tile.nodes)
        self.hexBoard = tmpBoard

    def assignTypes(self):
        resources = (['desert'] + ['hills'] * 3 + ['forest'] * 4 +
                    ['mountains'] * 3 + ['pasture'] * 4 + ['fields'] * 4)
        random.shuffle(resources)
        for row in range(len(self.hexBoard)):
            for col in range(len(self.hexBoard[0])):
                if (self.hexBoard[row][col] != None):
                    self.hexBoard[row][col].type = resources.pop()

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

class Tile(object):
    def __init__(self, r, q):
        self.pos = (r, q)
        self.number = None
        self.edges = []
        self.nodes = []
        self.type = None

    def __repr__(self):
        r = self.pos[0]
        q = self.pos[1]
        return f'<{self.type} Tile [{self.number}] at ({r}, {q})>'

class Edge(object):
    def __init__(self, id):
        self.road = None
        self.id = id
    
    def __repr__(self):
        return f'<Edge at id [{self.id}]>'
    
    def __eq__(self, other):
        return isinstance(other, Edge) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

class Node(object):
    def __init__(self, id, port=None):
        self.id = id
        self.port = port
        self.nodeLevel = None # 1 and 2 for settlement and city
    def __repr__(self):
        port = f'with Port {self.port}' if self.port != None else 'without a port' 
        return f'<Node at id [{self.id}], {port}>'