import copy
import curses
import logging

from .coordinates import Coordinates
from sprite.direction import Direction
from world.viewport import Viewport
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.timer import Timer
from utilities.color import Color

logger = logging.getLogger(__name__)


class Sprite(object):
    def __init__(
            self, 
            viewport :Viewport, 
            parentSprite, 
            coordinates :Coordinates =None,
            direction :Direction =Direction.none
    ):
        self.viewport = viewport
        self.parentSprite = parentSprite
        self.direction = direction
        self.texture = None

        self.coordinates = Coordinates(0, 0)
        if coordinates is not None:
            self.coordinates.x = coordinates.x
            self.coordinates.y = coordinates.y
        # For performance reason, we pre-allocate coords for use in getLocation()
        self.coordinatesRel = Coordinates(0, 0)

        self.active = True
        self.rendered = True

        # color related
        self.overwriteColorTimer = Timer(0.25, active=False)
        self.overwriteColor = None


    def setOverwriteColorFor(self, time :float, color :Color):
        if self.overwriteColorTimer.isActive():
            logger.debug("Color already active on new set color")
            return 

        self.overwriteColor = color

        self.overwriteColorTimer.setTimer(time)
        self.overwriteColorTimer.reset()


    def getLocation(self): 
        """Get a reference to our location.
        
        The location may depend on the parentSprite, if it is not None
        Note that we dont return a copy of the coordinates, but a reference 
        to an internal var.
        """
        if self.parentSprite is None: 
            return self.coordinates
        else:
            parentLocation = self.parentSprite.getLocation()
            self.coordinatesRel.x = parentLocation.x + self.coordinates.x
            self.coordinatesRel.y = parentLocation.y + self.coordinates.y
            return self.coordinatesRel


    def setLocation(self, coordinates :Coordinates):
        self.coordinates.x = coordinates.x
        self.coordinates.y = coordinates.y


    def advanceStep(self):
        if not self.isActive():
            return 

        self.texture.advanceStep()


    def advance(self, deltaTime :float): 
        if not self.isActive():
            return

        self.texture.advance(deltaTime)

        # reset overwrite color
        if self.overwriteColorTimer.timeIsUp():
            self.overwriteColor = None
            self.overwriteColorTimer.stop()
        self.overwriteColorTimer.advance(deltaTime)        


    def draw(self): 
        if not self.isActive():
            return 

        if not self.isRendered():
            return

        self.texture.draw(self.viewport)


    def collidesWithPoint(self, hitCoords :Coordinates):
        if hitCoords.x >= self.coordinates.x and hitCoords.x <= self.coordinates.x + self.texture.width:
            if hitCoords.y >= self.coordinates.y and hitCoords.y <= self.coordinates.y + self.texture.height:
                return True

        return False


    def isActive(self): 
        return self.active


    def setActive(self, active):
        self.active = active


    def isRendered(self): 
        return self.rendered
