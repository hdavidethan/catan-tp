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