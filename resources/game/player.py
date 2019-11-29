from config.colors import Colors

class Player(object):
    def __init__(self, index):
        self.index = index
        self.victoryPoints = 0
        self.longestRoad = 0
        self.largestArmy = 0
        self.roads = set()
        self.settlements = set()
        self.cities = set()
        self.devCards = {'knight':0, 'yearOfPlenty':0, 'monopoly':0, 'roadBuilding':0, 'victoryPoint':0}
        self.knights = set()
        self.bgColor, self.textColor = Colors.PLAYER[index]
        self.resources = {'lumber':0, 'sheep':0, 'brick':0, 'ore': 0, 'grain': 0}
        self.discardGoal = None
    
    # Counts the total number of cards of the player
    def countCards(self):
        return sum(self.resources.values())