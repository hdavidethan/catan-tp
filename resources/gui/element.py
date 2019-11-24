class Element(object):
    """
    Element takes pos, a tuple (x, y), and size, a tuple (width, height).
    """
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
    
    # Convert center to pygame coords
    def getRectArgs(self):
        cx, cy = self.pos
        width, height = self.size
        x0 = cx - width / 2
        y0 = cy - height / 2
        rectArgs = (x0, y0, width, height)
        return rectArgs
    
    def onClick(self, game):
        pass