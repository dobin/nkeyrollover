import copy
import curses
import logging

from .coordinates import Coordinates
from entities.direction import Direction

logger = logging.getLogger(__name__)


class Sprite(object): 
    def __init__(
            self, win, 
            parentSprite, 
            coordinates :Coordinates =Coordinates(),
            direction :Direction =Direction.none
    ):
        self.win = win
        self.parentSprite = parentSprite
        self.coordinates = coordinates
        self.direction = direction
        self.texture = None

        self.active = True
        self.rendered = True
        self.currentColor = None
        self.initColor()


    def setColor(self, color): 
        self.currentColor = color


    def initColor(self): 
        if self.win is None:
            # for simple unittests
            self.currentColor = 0

        # for unittests using MockWin
        # we always import 'curses', and dont know if we are being unittested
        # in the unittest, we use MockWin, which has method isUnitTest
        if hasattr(self.win, 'isUnitTest'):
            self.currentColor = 0

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

        self.texture.draw(self.win)


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
