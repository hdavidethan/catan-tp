import math
class CatanMath(object):
    # Draws an equilateral triangle from a hexagon outside the hexagon
    @staticmethod
    def getEqTriangle(screen, point1, point2, center):
        x1, y1 = point1
        x2, y2 = point2
        cx, cy = center
        dx = -(cx - x1)
        dy = -(cy - y1)
        newX = x2 + dx
        newY = y2 + dy
        return (point1, point2, (newX, newY))
    
    # Gets coordinates of all hexagon points
    @staticmethod
    def getHexagonPoints(bounds):
        x0, y0, x1, y1 = bounds
        width = x1 - x0
        height = y1 - y0
        point1 = (x0, y0 + height/4)
        point2 = (x0+width/2, y0)
        point3 = (x1, y0 + height/4)
        point4 = (x1, y0 + 3*height/4)
        point5 = (x0+width/2, y1)
        point6 = (x0, y0 + 3*height/4)
        return [point1, point2, point3, point4, point5, point6]
        