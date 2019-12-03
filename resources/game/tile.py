#########################################################################
# Tile File
# Contains Tile class; creates and stores Tiles and its contents
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

class Tile(object):
    def __init__(self, r, q):
        self.pos = (r, q)
        self.number = None
        self.edges = []
        self.nodes = []
        self.type = None
        self.hasRobber = False
        self.bounds = None

    def __repr__(self):
        r = self.pos[0]
        q = self.pos[1]
        return f'<{self.type} Tile [{self.number}] at ({r}, {q})>'
    
    def __eq__(self, other):
        return isinstance(other, Tile) and self.pos == other.pos
    
    def __hash__(self):
        return hash((self.pos,))