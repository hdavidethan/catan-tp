#########################################################################
# Colors File
# Contains the Color configurations for the entire Catan app
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

import pygame

class Colors(object):
    # Basic Colors
    WHITE = pygame.Color('0xffffff')
    BLACK = pygame.Color('0x000000')
    BLACK_ALPHA = pygame.Color('0x0000007b')
    BLACK_PAUSED = pygame.Color('0x000000ab')
    RED_1 = pygame.Color('0xe24e1b')
    RED_2 = pygame.Color('0xda7635')
    BLUE = pygame.Color('0x0097d3')

    # Menu Colors
    GOLD_1 = pygame.Color('0xfbbd08')
    GOLD_2 = pygame.Color('0xeaae00')
    GOLD_3 = pygame.Color('0xcd9903')
    GOLD_DISABLED = pygame.Color('0xf9dd86')

    # Tile Colors
    FOREST = pygame.Color('0x415c32')
    FIELDS = pygame.Color('0xc2ab4a')
    MOUNTAINS = pygame.Color('0x4d6066')
    HILLS = pygame.Color('0xaa4756')
    PASTURE = pygame.Color('0x94fa52')
    DESERT = pygame.Color('0xf2ee76')

    # Player Colors
    PLAYER = dict()
    PLAYER[0] = (pygame.Color('0xff9b42'), BLACK)
    PLAYER[1] = (pygame.Color('0x92140c'), WHITE)
    PLAYER[2] = (pygame.Color('0x002642'), WHITE)
    PLAYER[3] = (pygame.Color('0x8cb369'), BLACK)

    BUTTON_COLORS = [GOLD_1, GOLD_2, BLACK, GOLD_DISABLED, WHITE]