import pygame
from config.config import windowConfig
pygame.font.init()

sizeFactor = int(min(windowConfig.WIDTH, windowConfig.HEIGHT) / 600)

class Text(object):
    TOKEN_FONT = pygame.font.Font("resources/assets/minion-regular.ttf", 24*sizeFactor)
    PORT_FONT = pygame.font.Font("resources/assets/minion-regular.ttf", 16*sizeFactor)
    NODE_FONT = pygame.font.Font("resources/assets/minion-regular.ttf", 16*sizeFactor)
    SCORE_FONT = pygame.font.Font("resources/assets/minion-regular.ttf", 20*sizeFactor)
    CURRENT_PLAYER_FONT = pygame.font.Font("resources/assets/minion-regular.ttf", 20*sizeFactor)
    BUTTON_FONT = pygame.font.Font("resources/assets/cabin-regular.ttf", 22*sizeFactor)
    BUILD_FONT = pygame.font.Font("resources/assets/cabin-regular.ttf", 18*sizeFactor)
    RESOURCE_FONT = pygame.font.Font("resources/assets/minion-regular.ttf", 20*sizeFactor)
    ROBBER_FONT = pygame.font.Font("resources/assets/minion-regular.ttf", 20*sizeFactor)
    DISCARD_FONT = pygame.font.Font("resources/assets/cabin-regular.ttf", 18*sizeFactor)