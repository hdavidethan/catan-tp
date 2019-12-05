#########################################################################
# Player File
# Contains the Player class for the Catan Game
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

import copy, random
from config.colors import Colors

class Player(object):
    def __init__(self, index):
        self.index = index
        self.victoryPoints = 0
        self.longestRoad = 0
        self.hasLongestRoad = False
        self.largestArmy = 0
        self.hasLargestArmy = False
        self.roads = set()
        self.settlements = set()
        self.cities = set()
        self.devCards = {'knight':0, 'yearOfPlenty':0, 'monopoly':0, 'roadBuilding':0, 'victoryPoint':0}
        self.bgColor, self.textColor = Colors.PLAYER[index]
        self.resources = {'lumber':0, 'sheep':0, 'brick':0, 'ore': 0, 'grain': 0}
        self.discardGoal = None
    
    # Counts the total number of cards of the player
    def countCards(self):
        return sum(self.resources.values())
    
    def countRoads(self, game):
        maxLength = 0
        for roadID in self.roads:
            length = self.checkRoads(roadID, game, set())
            maxLength = max(length, maxLength)
        return maxLength + 1 if self.roads != set() else 0

    def checkRoads(self, roadID, game, checked):
        length = len(checked)
        road = game.board.edges[roadID]
        node1, node2 = road.getNodes(game.board)
        tmp1 = list(node1.getRoads(game.board))
        tmp1.remove(roadID)
        roads = copy.copy(tmp1)
        for branchID in roads:
            branchRoad = game.board.edges[branchID]
            if (branchRoad.road == self.bgColor):
                if (branchID not in checked):
                    newChecked = copy.copy(checked)
                    newChecked.add(branchID)
                    testLength = self.checkRoads(branchID, game, newChecked)
                    length = max(length, testLength)
        return length
    
    def getOwnedNodes(self):
        total = set()
        for node in self.settlements:
            total.add(node)
        for node in self.cities:
            total.add(node)
        return total

