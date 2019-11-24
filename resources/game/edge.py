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