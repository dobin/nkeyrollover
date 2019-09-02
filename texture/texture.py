import copy
import logging

from sprite.coordinates import Coordinates
from sprite.sprite import Sprite

logger = logging.getLogger(__name__)


class Texture(object):
    def __init__(self, parentSprite :Sprite, width =0, height =0, offset =None):
        self.parentSprite :Sprite =parentSprite
        self.width :int = width
        self.height :int = height
        self.active :bool = True
        self.offset :Coordinates = Coordinates()
        if offset is not None:
            self.offset.x = offset.x
            self.offset.y = offset.y
        # For performance reason, we pre-allocate coords for use in getLocation()
        self.offsetRel :Coordinates = Coordinates()


    def draw(self, viewport):
        pass


    def advance(self, deltaTime :float):
        pass


    def advanceStep(self):
        pass


    def setActive(self, active :bool):
        self.active = active


    def isActive(self) -> bool:
        return self.active


    def getLocation(self):
        """Get a reference to our location.

        The location may depend on the parentSprite, if it is not None
        Note that we dont return a copy of the coordinates, but a reference
        to an internal var.
        """
        if self.parentSprite is None:
            return self.offset
        else:
            parentLocation = self.parentSprite.getLocation()
            self.offsetRel.x = parentLocation.x + self.offset.x
            self.offsetRel.y = parentLocation.y + self.offset.y
            return self.offsetRel


    def getTextureHitCoordinates(self, animationIdx=0):
        # ani = self.animation[ animationIdx ]
        locations = []
        baseLocation = self.getLocation()
        x = 0
        while x < self.width:
            y = 0
            while y < self.height:
                # expensive copy, but its only on-hit
                loc = copy.copy(baseLocation)
                loc.x += x
                loc.y += y
                locations.append(loc)

                y += 1

            x += 1

        return locations


    def setLocation(self, x, y):
        self.offset.x = x
        self.offset.y = y
