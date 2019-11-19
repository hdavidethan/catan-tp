class Element(object):
    """
    Element takes pos, a tuple (x, y), and size, a tuple (width, height).
    """
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size