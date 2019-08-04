import logging
import curses 

from .entitytype import EntityType
from .direction import Direction
from utilities.timer import Timer

logger = logging.getLogger(__name__)


class Entity(object):
    def __init__(self, win, parent, entityType):
        self.win = win
        self.parent = parent
        self.sprite = None
        self.entityType = entityType

        # the director will remove figure from the Alive list if this is false
        # making us unrenderable, and unadvancable (aka when truly dead)
        self.isActive = True
        self.isRendered = True

        self.x = 0
        self.y = 0
        self.offsetX = 0
        self.offsetY = 0
        self.direction = Direction.right

        self.baseColor = self.getColorByType(self.entityType)
        self.currentColor = self.baseColor
        self.colorTimer = Timer(0.25, active=False)

        # timer for deactivation of this entity
        self.durationTimer = Timer(0.0, active=False)


    def getColorByType(self, type):
        if type is EntityType.player: 
            return curses.color_pair(1)
        elif type is EntityType.enemy:
            return curses.color_pair(2)
        elif type is EntityType.takedamage:
            return curses.color_pair(3)
        elif type is EntityType.weapon:
            return curses.color_pair(4)
        else: 
            logging.error("unknown color type: " + str(type))
            return curses.color_pair(1)


    def setColorFor(self, time, type):
        if self.colorTimer.isActive():
            logging.warn("Color already active on new set color")
            return 

        newColor = self.getColorByType(type)
        self.currentColor = newColor

        if time > 0.0:
            self.colorTimer.setTimer(time)
            self.colorTimer.reset()
        else: 
            self.baseColor = self.currentColor


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


    def advance(self, deltaTime):
        if not self.isActive: 
            return

        # reset color
        if self.colorTimer.timeIsUp():
            self.currentColor = self.baseColor
            self.colorTimer.stop()
        self.colorTimer.advance(deltaTime)

        self.sprite.advance(deltaTime)

        self.durationTimer.advance(deltaTime)

        if self.durationTimer.isActive() and self.durationTimer.timeIsUp():
            self.setActive(False)


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