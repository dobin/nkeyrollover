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

        # timer for deactivation of this entity
        self.durationTimer = Timer(0.0, active=False)


    def advance(self, deltaTime):
        super(Entity, self).advance(deltaTime)
        self.durationTimer.advance(deltaTime)

        if self.durationTimer.isActive() and self.durationTimer.timeIsUp():
            self.setActive(False)



