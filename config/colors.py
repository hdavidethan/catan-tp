import pygame

class Colors(object):
    # Basic Colors
    WHITE = pygame.Color('0xffffff')
    BLACK = pygame.Color('0x000000')
    RED_1 = pygame.Color('0xe24e1b')
    RED_2 = pygame.Color('0xda7635')

    # Menu Colors
    GOLD_1 = pygame.Color('0xfbbd08')
    GOLD_2 = pygame.Color('0xeaae00')
    GOLD_3 = pygame.Color('0xcd9903')

    # Tile Colors
    FOREST = pygame.Color('0x415c32')
    FIELDS = pygame.Color('0xc2ab4a')
    MOUNTAINS = pygame.Color('0x4d6066')
    HILLS = pygame.Color('0x9c1428')
    PASTURE = pygame.Color('0x94fa52')
    DESERT = pygame.Color('0xf2ee76')

    # Player Colors
    PLAYER = dict()
    PLAYER[0] = (pygame.Color('0xd0f2e3'), BLACK)
    PLAYER[1] = (pygame.Color('0x92140c'), WHITE)
    PLAYER[2] = (pygame.Color('0x002642'), WHITE)
    PLAYER[3] = (pygame.Color('0x8cb369'), BLACK)