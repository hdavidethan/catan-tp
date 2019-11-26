#########################################################################
# Config File
# Contains utility functions, i.e. Math
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

import math, random
from config.colors import Colors

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
    
    # Get the dimensions of a thick anti-aliased line
    # Based on solution by Yannis Assael
    # https://stackoverflow.com/questions/30578068/pygame-draw-anti-aliased-thick-line
    @staticmethod
    def getThickAALine(point1, point2, thickness=3):
        x1, y1 = point1
        x2, y2 = point2
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        length = CatanMath.distance(point1, point2)
        angle = math.atan2(y1-y2, x1-x2)
        # Dimension calculations
        upperLeft = (cx + (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
                    cy + (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
        upperRight = (cx - (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
                    cy + (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
        bottomLeft = (cx + (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
                    cy - (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
        bottomRight = (cx - (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
                    cy - (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
        return (upperLeft, upperRight, bottomRight, bottomLeft)

    @staticmethod
    def distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Utils(object):
    # Returns the resource name from the type of tile
    @staticmethod
    def getResourceFromType(type):
        resources = {'forest':'lumber', 'desert':None,
                    'hills':'brick', 'mountains':'ore',
                    'pasture':'sheep', 'fields':'grain',
                    None:None}
        return resources[type]
    
    @staticmethod
    def stealRandomResource(victim):
        validSteals = ['lumber', 'brick', 'ore', 'sheep', 'grain']
        for key in victim.resources:
            if (victim.resources[key] == 0):
                validSteals.remove(key)
        return random.choice(validSteals)
    
    @staticmethod
    def getProbabilityFromNumber(n):
        probabilities = {2:1, 3:2, 4:3, 5:4, 6:5, 8:5, 9:4, 10:3, 11:2, 12:1}
        return probabilities[n]

    # @staticmethod
    # def getPlayerFromColor(players, color):
    #     player = None
    #     for key in Colors.PLAYER:
    #         if (Colors.PLAYER[key][0] == color):
    #             player = key
    #         print(player, Colors.PLAYER[key][0], color)
    #     return players[player] if player is not None else None
        