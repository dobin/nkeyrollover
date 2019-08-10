import logging
import curses 
from .entitytype import EntityType
from sprite.direction import Direction
from utilities.timer import Timer
from sprite.sprite import Sprite
from sprite.coordinates import Coordinates
from world.viewport import Viewport
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType

logger = logging.getLogger(__name__)


class Entity(Sprite):
    def __init__(self, viewport, parentSprite :Sprite, entityType :EntityType):
        super(Entity, self).__init__(
            viewport=viewport, parentSprite=parentSprite, coordinates =Coordinates(),
            direction=Direction.right)

        self.entityType = entityType

        self.baseColor = self.getColorByType(self.entityType)
        self.currentColor = self.baseColor
        self.colorTimer = Timer(0.25, active=False)

        # timer for deactivation of this entity
        self.durationTimer = Timer(0.0, active=False)


    def getColorByType(self, type):
        return ColorPalette.getColorByEntityType(type, self.viewport)


    def setColorFor(self, time, type):
        if self.colorTimer.isActive():
            logger.debug("Color already active on new set color")
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



