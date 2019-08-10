import copy
import curses
import logging

from .coordinates import Coordinates
from sprite.direction import Direction
from world.viewport import Viewport

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

        self.active = True
        self.rendered = True
        self.currentColor = None
        self.initColor()


    def setColor(self, color): 
        self.currentColor = color


    def initColor(self): 
        if self.viewport is None:
            # for simple unittests
            self.currentColor = 0
            return

        # for unittests using MockWin
        # we always import 'curses', and dont know if we are being unittested
        # in the unittest, we use MockWin, which has method isUnitTest
        if hasattr(self.viewport, 'isUnitTest'):
            self.currentColor = 0
            return 

        self.setColor(curses.color_pair(1))


    def getLocation(self): 
        """Get a copy of the location
        
        The location may depend on the parentSprite, if it is not None
        """
        if self.parentSprite is None: 
            return copy.copy(self.coordinates)
        else: 
            loc = copy.copy(self.parentSprite.getLocation())
            loc.x += self.coordinates.x
            loc.y += self.coordinates.y
            return loc


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
