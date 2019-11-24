import pygame
from resources.gui.element import Element
from config.colors import Colors
from config.text import Text

class Scorecard(Element):
    def __init__(self, player, pos, size):
        self.player = player
        self.pos = pos
        self.size = size
    
    def __eq__(self, other):
        return isinstance(other, Scorecard) and (self.player == other.player)
    
    def __hash__(self):
        return hash((self.player, self.pos, self.size))
    
    def draw(self, screen):
        x, y = self.pos
        width, height = self.size
        pygame.draw.rect(screen, self.player.bgColor, (x, y, width, height))
        pygame.draw.rect(screen, Colors.BLACK, (x, y, width, height), 1)
        dy = height / 4
        text = [f'VP: {self.player.victoryPoints}', f'LR: {self.player.longestRoad}', f'LA: {self.player.largestArmy}']
        labels = []
        for i in range(3):
            label = Text.SCORE_FONT.render(text[i], True, self.player.textColor)
            labelPos = label.get_rect()
            labelPos.centery = y + (i + 1) * dy
            labelPos.left = x + 0.65 * width
            labels.append((label, labelPos))
        for t in labels:
            screen.blit(t[0], t[1])
        playerIndex = self.player.index + 1
        playerLabel = Text.SCORE_FONT.render(f'Player {playerIndex}', True, self.player.textColor)
        playerPos = playerLabel.get_rect()
        playerPos.centery = y + dy
        playerPos.left = x + 0.1 * width
        screen.blit(playerLabel, playerPos)
        cards = self.player.countCards()
        cardColor = self.player.textColor
        if (cards > 7):
            if (cardColor == Colors.BLACK):
                cardColor = Colors.RED_1
            else:
                cardColor = Colors.RED_2
        cardLabel = Text.SCORE_FONT.render(f'{cards} Cards', True, cardColor)
        cardPos = cardLabel.get_rect()
        cardPos.centery = y + 3 * dy
        cardPos.left = x + 0.1 * width
        screen.blit(cardLabel, cardPos)