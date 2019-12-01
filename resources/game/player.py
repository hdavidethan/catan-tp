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

    # TODO: Make this recursive
    # i.e. do two halves and have each possible segment return a list of roads connected
    def checkLongestRoad(self, player):
        pass
        # TODO: ALl following code is indented 1 tab to the right.
        #     if (len(player.roads) >= 5):
        #         mainSet = copy.copy(player.roads)
        #         seen = set()
        #         first = random.choice(list(mainSet))
        #         mainSet.remove(first)
        #         seen.add(first)
        
        # def recursiveLongestRoad(self, player):
        #     if ():
        #         pass
        #     else:
        #         road1, road2 = first.getRoads(self.board)
        #         for edge in road1:
        #             if (self.board.edges[edge] in mainSet):
        #                 seen.add(self.board.edges[edge])
        #         for edge in road2:
        #             if (self.board.edges[edge] in mainSet):
        #                 seen.add(self.board.edges[edge])