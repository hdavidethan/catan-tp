class Node(object):
    def __init__(self, id, port=None):
        self.id = id
        self.port = port
        self.nodeLevel = None # 1 and 2 for settlement and city
    def __repr__(self):
        port = f'with Port {self.port}' if self.port != None else 'without a port' 
        return f'<Node at id [{self.id}], {port}>'