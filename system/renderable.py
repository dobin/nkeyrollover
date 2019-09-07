from __future__ import annotations
# this so i can give type information about my own class
# https://stackoverflow.com/questions/33533148/how-do-i-specify-that-the-return-type-of-a-method-is-the-same-as-the-class-itsel

import copy
import logging
from typing import List

from sprite.coordinates import Coordinates, ExtCoordinates
from sprite.direction import Direction
from messaging import messaging, Messaging, Message, MessageType
from config import Config
from texture.texture import Texture
from world.viewport import Viewport

logger = logging.getLogger(__name__)


class Renderable(object):
    def __init__(
        self,
        texture :Texture,
        viewport :Viewport,
        parent :Renderable =None,
        coordinates :Coordinates =None,
        z :int =0,
        active :bool =True,
        useParentDirection =False,
    ):
        self.viewport :Viewport = viewport
        self.texture :Texture = texture

        # if parent is given, this position will always be relative
        # to that parent
        self.parent :Renderable = parent

        # some things, like weapon, need to be on the correct
        # side of the parent
        self.useParentDirection = useParentDirection

        # if this is being rendered
        self.active :bool = active

        # coordinates
        self.coordinates :Coordinates = Coordinates(0, 0)
        if coordinates is not None:
            self.coordinates.x = coordinates.x
            self.coordinates.y = coordinates.y
        # For performance reason, we pre-allocate coords for use in getLocation()
        self.coordinatesRel :Coordinates = Coordinates(0, 0)
        self.coordinatesRel2 :Coordinates = Coordinates(0, 0)
        self.z :int = z

        self.direction = Direction.left
        self.name = 'none'


    def __repr__(self):
        return self.name


    def getLocationAndSize(self):
        loc = self.getLocation()

        d = ExtCoordinates(
            x=loc.x,
            y=loc.y,
            width=self.texture.width,
            height=self.texture.height
        )
        return d


    def getLocation(self):
        """Get a reference to our location.

        The location may depend on the parentSprite, if it is not None
        Note that we dont return a copy of the coordinates, but a reference
        to an internal var.
        """
        if self.parent is None:
            return self.coordinates
        else:
            parentLocation = self.parent.getLocation()
            if self.parent.direction is Direction.left or not self.useParentDirection:
                self.coordinatesRel.x = parentLocation.x + self.coordinates.x
                self.coordinatesRel.y = parentLocation.y + self.coordinates.y
            else:
                self.coordinatesRel.x = parentLocation.x + (-1 * self.coordinates.x) + self.parent.texture.width - self.texture.width
                self.coordinatesRel.y = parentLocation.y + self.coordinates.y
            return self.coordinatesRel


    def getLocationDirectionInverted(self):
        if self.parent is None:
            return self.coordinates
        else:
            parentLocation = self.parent.getLocation()
            if self.parent.direction is Direction.right:
                self.coordinatesRel2.x = parentLocation.x + self.coordinates.x
                self.coordinatesRel2.y = parentLocation.y + self.coordinates.y
            else:
                self.coordinatesRel2.x = parentLocation.x + (-1 * self.coordinates.x) + self.parent.texture.width - self.texture.width
                self.coordinatesRel2.y = parentLocation.y + self.coordinates.y
            return self.coordinatesRel2


    def setLocation(self, coordinates :Coordinates):
        self.coordinates.x = coordinates.x
        self.coordinates.y = coordinates.y


    def getLocationCenter(self):
        # slow, but its currently only used by rare events like skillExplosion
        loc = copy.copy(self.getLocation())
        # this will round down
        loc.x += int(self.texture.width / 2)
        loc.y += int(self.texture.height / 2)
        return loc


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

        self.texture.draw(self.viewport, self.getLocation())


    def isHitBy(self, hitLocations :List[Coordinates]):
        for hitLocation in hitLocations:
            if self.collidesWithPoint(hitLocation):
                return True

        return False


    def collidesWithPoint(self, hitCoords :Coordinates):
        if hitCoords.x >= self.coordinates.x and hitCoords.x < self.coordinates.x + self.texture.width:
            if hitCoords.y >= self.coordinates.y and hitCoords.y < self.coordinates.y + self.texture.height:
                return True

        return False


    def getWeaponBaseLocation(self):
        # Slow
        loc = copy.copy(self.getLocation())

        loc.y -= 1
        if self.direction is Direction.left:
            loc.x -= -1
        else:
            loc.x += self.texture.width + -1

        return loc


    def getAttackBaseLocation(self):
        # Slow
        loc = copy.copy(self.getLocation())

        loc.y += 1
        if self.direction is Direction.left:
            loc.x -= 1
        else:
            loc.x += self.texture.width + 1

        return loc


    def getTextureHitCoordinates(self, animationIdx=0):
        locations = self.texture.getTextureHitCoordinates(animationIdx=0)
        baseLocation = self.getLocation()

        # make relative coordinates absolute
        for location in locations:
            location.x += baseLocation.x
            location.y += baseLocation.y

        return locations


    def isActive(self):
        return self.active


    def setActive(self, active):
        self.active = active


    def getDirection(self):
        return self.direction
