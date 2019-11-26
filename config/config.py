#########################################################################
# Config File
# Contains function variables used as constants for more organized access
# Written by David Hwang (dchwang) for 15-112 Fall 2019 Term Project
#########################################################################

class windowConfig(object):
    # Window Size
    WIDTH = 900
    HEIGHT = 600
    sizeFactor = min(WIDTH, HEIGHT)
    HEIGHT_TO_WIDTH_RATIO = 32 / 35

    # Button Positions
    MENU_B1 = (0.5 * WIDTH, 0.5 * HEIGHT)
    MENU_B1_SIZE = (0.25 * WIDTH, 0.085 * HEIGHT)
    MENU_B2 = (0.5 * WIDTH, 0.72 * HEIGHT)
    MENU_B2_SIZE = (0.25 * WIDTH, 0.085 * HEIGHT)
    MENU_B3 = (0.5 * WIDTH, 0.61 * HEIGHT)

    # Logo
    LOGO = (0.5 * WIDTH, 0.25 * HEIGHT)
    LOGO_SCALE = 0.2

    # Menu Container
    MENU_CONTAINER = (0.34 * WIDTH, 0.4 * HEIGHT)
    MENU_CONTAINER_SIZE = (0.32 * WIDTH, 0.42 * HEIGHT)

    # Game Scorecards
    SCORE_1 = (0, 0.8 * HEIGHT)
    SCORE_2 = (0, 0)
    SCORE_3 = (0.8 * WIDTH, 0)
    SCORE_4 = (0.8 * WIDTH, 0.8 * HEIGHT)
    SCORE_SIZE = (0.2 * WIDTH, 0.2 * HEIGHT)

    # GUI
    CURRENT_PLAYER = (0.98 * WIDTH, 0.705 * HEIGHT)
    END_TURN = (0.9 * WIDTH, 0.76 * HEIGHT)
    END_TURN_SIZE = (0.18 * WIDTH, 0.05 * HEIGHT)
    
    DICE_1 = (0.84 * WIDTH, 0.25 * HEIGHT)
    DICE_2 = (0.9 * WIDTH, 0.25 * HEIGHT)
    DICE_SIZE = (0.06 * sizeFactor, 0.06 * sizeFactor)

    RESOURCES = (0.28 * WIDTH, 0.95 * HEIGHT)
    RESOURCES_SIZE = (0.44 * WIDTH, 0.05 * HEIGHT)

    BUILD = dict()
    BUILD['road'] = (0.1 * WIDTH, 0.55 * HEIGHT)
    BUILD['settlement'] = (0.1 * WIDTH, 0.62 * HEIGHT)
    BUILD['city'] = (0.1 * WIDTH, 0.69 * HEIGHT)
    BUILD['devCard'] = (0.1 * WIDTH, 0.76 * HEIGHT)
    BUILD_SIZE = (0.18 * WIDTH, 0.05 * HEIGHT)

    SELECT_BUTTON_SIZE = (0.025 * sizeFactor, 0.025 * sizeFactor)

    DISCARD = dict()
    DISCARD['lumber'] = (0.35 * WIDTH, 0.92 * HEIGHT)
    DISCARD['brick'] = (0.42 * WIDTH, 0.92 * HEIGHT)
    DISCARD['sheep'] = (0.49 * WIDTH, 0.92 * HEIGHT)
    DISCARD['grain'] = (0.56 * WIDTH, 0.92 * HEIGHT)
    DISCARD['ore'] = (0.63 * WIDTH, 0.92 * HEIGHT)

    STEAL = dict()
    STEAL[0] = (0.25 * WIDTH, 0.82 * HEIGHT)
    STEAL[1] = (0.25 * WIDTH, 0.18 * HEIGHT)
    STEAL[2] = (0.75 * WIDTH, 0.18 * HEIGHT)
    STEAL[3] = (0.75 * WIDTH, 0.82 * HEIGHT)
    STEAL_SIZE = (0.08 * WIDTH, 0.05 * HEIGHT)

    DISCARD_SIZE = (0.04 * sizeFactor, 0.04 * sizeFactor)