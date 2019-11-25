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
        self.bgColor, self.textColor = Colors.PLAYER[index]
        self.resources = {'lumber':0, 'sheep':0, 'brick':0, 'ore': 0, 'grain': 0}
        self.discardGoal = None
    
    # Counts the total number of cards of the player
    def countCards(self):
        return sum(self.resources.values())