class windowConfig(object):
    # Window Size
    WIDTH = 900
    HEIGHT = 600

    # Button Positions
    MENU_B1 = (0.5 * WIDTH, 0.5 * HEIGHT)
    MENU_B1_SIZE = (0.25 * WIDTH, 0.085 * HEIGHT)
    MENU_B2 = (0.5 * WIDTH, 0.75 * HEIGHT)
    MENU_B2_SIZE = (0.25 * WIDTH, 0.085 * HEIGHT)

    # Game Scorecards
    SCORE_1 = (0, 0.8 * HEIGHT)
    SCORE_2 = (0, 0)
    SCORE_3 = (0.8 * WIDTH, 0)
    SCORE_4 = (0.8 * WIDTH, 0.8 * HEIGHT)
    SCORE_SIZE = (0.2 * WIDTH, 0.2 * HEIGHT)

    # GUI
    CURRENT_PLAYER = (0.82 * WIDTH, 0.705 * HEIGHT)
    END_TURN = (0.9 * WIDTH, 0.76 * HEIGHT)
    END_TURN_SIZE = (0.18 * WIDTH, 0.05 * HEIGHT)
    
    sizeFactor = min(WIDTH, HEIGHT)
    DICE_1 = (0.84 * WIDTH, 0.25 * HEIGHT)
    DICE_2 = (0.9 * WIDTH, 0.25 * HEIGHT)
    DICE_SIZE = (0.06 * sizeFactor, 0.06 * sizeFactor)

    RESOURCES = (0.3 * WIDTH, 0.95 * HEIGHT)
    RESOURCES_SIZE = (0.4 * WIDTH, 0.05 * HEIGHT)
