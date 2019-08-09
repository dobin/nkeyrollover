import logging
import curses 
from .entitytype import EntityType
from sprite.direction import Direction
from utilities.timer import Timer
from sprite.sprite import Sprite
from sprite.coordinates import Coordinates

logger = logging.getLogger(__name__)


class Entity(Sprite):
    def __init__(self, win, parentSprite :Sprite, entityType :EntityType):
        super(Entity, self).__init__(
            win=win, parentSprite=parentSprite, coordinates =Coordinates(),
            direction=Direction.right)

        self.entityType = entityType

        self.baseColor = self.getColorByType(self.entityType)
        self.currentColor = self.baseColor
        self.colorTimer = Timer(0.25, active=False)

        # timer for deactivation of this entity
        self.durationTimer = Timer(0.0, active=False)


    def getColorByType(self, type):
        if self.win is None:
            # for simple unittests
            return

        # for unittests using MockWin
        # we always import 'curses', and dont know if we are being unittested
        # in the unittest, we use MockWin, which has method isUnitTest
        if hasattr(self.win, 'isUnitTest'):
            return 0

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


    def advance(self, deltaTime):
        super(Entity, self).advance(deltaTime)

        # reset color
        if self.colorTimer.timeIsUp():
            self.currentColor = self.baseColor
            self.colorTimer.stop()
        self.colorTimer.advance(deltaTime)

        self.durationTimer.advance(deltaTime)

        if self.durationTimer.isActive() and self.durationTimer.timeIsUp():
            self.setActive(False)



