#########################################################################
# Text File
# Contains text and font configurations for the app
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

import pygame
from config.config import windowConfig
pygame.font.init()

sizeFactor = int(min(windowConfig.WIDTH, windowConfig.HEIGHT) / 600)

class Text(object):
    TOKEN_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 24*sizeFactor)
    PORT_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 16*sizeFactor)
    NODE_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 18*sizeFactor)
    SCORE_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 20*sizeFactor)
    CURRENT_PLAYER_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 20*sizeFactor)
    BUTTON_FONT = pygame.font.Font("resources/assets/fonts/cabin-regular.ttf", 22*sizeFactor)
    BUILD_FONT = pygame.font.Font("resources/assets/fonts/cabin-regular.ttf", 18*sizeFactor)
    RESOURCE_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 20*sizeFactor)
    ROBBER_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 20*sizeFactor)
    DISCARD_FONT = pygame.font.Font("resources/assets/fonts/cabin-regular.ttf", 18*sizeFactor)
    STEAL_FONT = pygame.font.Font("resources/assets/fonts/cabin-regular.ttf", 18*sizeFactor)
    PAUSED_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 36*sizeFactor)
    VICTORY_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 36*sizeFactor)
    SETUP_TITLE_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 36*sizeFactor)
    SETUP_COUNT_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 24*sizeFactor)
    SETUP_LABEL_FONT = pygame.font.Font("resources/assets/fonts/minion-regular.ttf", 28*sizeFactor)
    INC_DEC_FONT = pygame.font.Font("resources/assets/fonts/cabin-regular.ttf", 28*sizeFactor)

    # Text Constants
    BUILD = dict()
    BUILD['road'] = "Build Road"
    BUILD['settlement'] = "Build Settlement"
    BUILD['city'] = "Build City"
    BUILD['devCard'] = "Buy Dev Card"