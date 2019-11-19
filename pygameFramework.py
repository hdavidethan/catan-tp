#########################################################################
# Pygame Framework
# Adapted from http://blog.lukasperaza.com/getting-started-with-pygame/
# Original code by Lukas Peraza
# Modified with code from cmu_112_graphics.py (ver. 0.8.5)
#########################################################################

import pygame

class PygameGame(object):

    """
    a bunch of stuff is left out of this file, but you can check it out in the Github repo
    """
    def redrawAll(self, screen): pass
    def init(self): pass
    def keyPressed(self, key, mod): pass
    def keyReleased(self, key, mod): pass
    def mousePressed(self, pos1, pos2): pass
    def mouseReleased(self, pos1, pos2): pass
    def mouseMotion(self, pos1, pos2): pass
    def mouseDrag(self, pos1, pos2): pass
    def timerFired(self, time): pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=50, title="Pygame Window"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self._running = True
        self._paused = False
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        while self._running:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    self._running = False
            screen.fill((255, 255, 255))
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()