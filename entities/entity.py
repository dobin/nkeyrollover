from .direction import Direction

import logging

logger = logging.getLogger(__name__)

class Entity(object):
    def __init__(self, win, parent, coordinates):
        self.win = win
        self.parent = parent
        self.sprite = None

        # the director will remove figure from the Alive list if this is false
        # making us unrenderable, and unadvancable (aka when truly dead)
        self.isActive = True
        self.isRendered = True

        self.x = 0
        self.y = 0
        self.offsetX = 0
        self.offsetY = 0
        self.direction = Direction.right

        # timer for deactivation of this entity
        self.duration = 0
        self.durationLeft = 0


    def getLocation(self): 
        if self.parent is None: 
            loc = {
                'x': self.x,
                'y': self.y,
            }
            return loc
        else: 
            loc = self.parent.getLocation()
            loc['x'] += self.offsetX
            loc['y'] += self.offsetY
            return loc



    def advanceStep(self):
        if not self.isActive: 
            return 

        self.sprite.advanceStep()


    def advance(self):
        if not self.isActive: 
            return 

        self.sprite.advance()

        if self.durationLeft > 0:
            self.durationLeft = self.durationLeft - 1
            if self.durationLeft == 0:
                self.isActive = False


    def draw(self, win):
        if not self.isActive:
            return 

        if not self.isRendered:
            return

        self.sprite.draw(win)


    def collidesWithPoint(self, hitCoords):
        # TODO make this more generic, not just for simple 3x3
        if hitCoords['x'] >= self.x and hitCoords['x'] <= self.x + 3:
            if hitCoords['y'] >= self.y and hitCoords['y'] <= self.y + 3:
                return True

        return False


    def setActive(self, isActive):
        self.isActive = isActive