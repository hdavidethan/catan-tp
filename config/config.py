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
    MENU_B1 = (0.5 * WIDTH, 0.54 * HEIGHT)
    MENU_B2 = (0.5 * WIDTH, 0.68 * HEIGHT)
    MENU_SIZE = (0.25 * WIDTH, 0.085 * HEIGHT)

    # Logo
    LOGO = (0.5 * WIDTH, 0.25 * HEIGHT)
    LOGO_SCALE = 0.2

    # Menu Container
    MENU_CONTAINER = (0.34 * WIDTH, 0.44 * HEIGHT)
    MENU_CONTAINER_SIZE = (0.32 * WIDTH, 0.34 * HEIGHT)

    # Setup Container
    SETUP_CONTAINER = (0.15 * WIDTH, 0.4 * HEIGHT)
    SETUP_CONTAINER_SIZE = (0.7 * WIDTH, 0.5 * HEIGHT)
    SETUP_TITLE = (0.5 * WIDTH, 0.47 * HEIGHT)
    SETUP_HUMAN = (0.35 * WIDTH, 0.58 * HEIGHT)
    SETUP_HUMAN_COUNT = (0.35 * WIDTH, 0.65 * HEIGHT)
    SETUP_AI = (0.65 * WIDTH, 0.58 * HEIGHT)
    SETUP_AI_COUNT = (0.65 * WIDTH, 0.65 * HEIGHT)

    # Setup Buttons
    SETUP_HUMAN_DEC = (0.3 * WIDTH, 0.65 * HEIGHT)
    SETUP_HUMAN_INC = (0.4 * WIDTH, 0.65 * HEIGHT)
    SETUP_AI_DEC = (0.6 * WIDTH, 0.65 * HEIGHT)
    SETUP_AI_INC = (0.7 * WIDTH, 0.65 * HEIGHT)
    SETUP_INC_DEC_SIZE = (0.05 * sizeFactor, 0.05 * sizeFactor)
    SETUP_CONFIRM = (0.5 * WIDTH, 0.8 * HEIGHT)
    SETUP_CONFIRM_SIZE = (0.25 * WIDTH, 0.075 * HEIGHT)

    # Pause Menu Buttons
    PAUSE_RESUME = (0.5 * WIDTH, 0.5 * HEIGHT)
    PAUSE_RESTART = (0.5 * WIDTH, 0.64 * HEIGHT)
    PAUSE_QUIT = (0.5 * WIDTH, 0.78 * HEIGHT)
    PAUSE_SIZE = (0.25 * WIDTH, 0.085 * HEIGHT)

    # Victory Buttons
    VICTORY_RESTART = (0.5 * WIDTH, 0.64 * HEIGHT)
    VICTORY_QUIT = (0.5 * WIDTH, 0.78 * HEIGHT)
    VICTORY_SIZE = (0.25 * WIDTH, 0.085 * HEIGHT)

    # Game Scorecards
    SCORE_1 = (0, 0.8 * HEIGHT)
    SCORE_2 = (0, 0)
    SCORE_3 = (0.78 * WIDTH, 0)
    SCORE_4 = (0.78 * WIDTH, 0.8 * HEIGHT)
    SCORE_SIZE = (0.22 * WIDTH, 0.2 * HEIGHT)

    # GUI
    CURRENT_PLAYER = (0.98 * WIDTH, 0.705 * HEIGHT)
    END_TURN = (0.9 * WIDTH, 0.76 * HEIGHT)
    END_TURN_SIZE = (0.18 * WIDTH, 0.05 * HEIGHT)

    ROBBER_SCALE = 0.25
    
    DICE_1 = (0.84 * WIDTH, 0.25 * HEIGHT)
    DICE_2 = (0.9 * WIDTH, 0.25 * HEIGHT)
    DICE_SIZE = (0.06 * sizeFactor, 0.06 * sizeFactor)

    RESOURCES = (0.28 * WIDTH, 0.95 * HEIGHT)
    RESOURCES_SIZE = (0.44 * WIDTH, 0.05 * HEIGHT)

    DEVCARDS = (0.27 * WIDTH, 0)
    DEVCARDS_SIZE = (0.46 * WIDTH, 0.05 * HEIGHT)
    USE_DEVCARD = (0.1 * WIDTH, 0.24 * HEIGHT)
    USE_DEVCARD_SIZE = (0.18 * WIDTH, 0.05 * HEIGHT)

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

    DEVCARD_CHOICE = dict()
    DEVCARD_CHOICE['knight'] = (0.45 * WIDTH, 0.08 * HEIGHT)
    DEVCARD_CHOICE['yearOfPlenty'] = (0.55 * WIDTH, 0.08 * HEIGHT)
    # DEVCARD_CHOICE['monopoly'] = (0.55 * WIDTH, 0.08 * HEIGHT)
    # DEVCARD_CHOICE['roadBuilding'] = (0.65 * WIDTH, 0.08 * HEIGHT)
    DEVCARD_CHOICE_SIZE = (0.04 * sizeFactor, 0.04 * sizeFactor)

    STEAL = dict()
    STEAL[0] = (0.27 * WIDTH, 0.82 * HEIGHT)
    STEAL[1] = (0.27 * WIDTH, 0.18 * HEIGHT)
    STEAL[2] = (0.72 * WIDTH, 0.18 * HEIGHT)
    STEAL[3] = (0.72 * WIDTH, 0.82 * HEIGHT)
    STEAL_SIZE = (0.08 * WIDTH, 0.05 * HEIGHT)

    DISCARD_SIZE = (0.04 * sizeFactor, 0.04 * sizeFactor)