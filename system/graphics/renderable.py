from __future__ import annotations
# this so i can give type information about my own class
# https://stackoverflow.com/questions/33533148/how-do-i-specify-that-the-return-type-of-a-method-is-the-same-as-the-class-itsel

import copy
import logging
from typing import List

from common.coordinates import Coordinates, ExtCoordinates
from common.direction import Direction
from texture.texture import Texture
from game.viewport import Viewport

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
        direction=Direction.left,
        name=''
    ):
        self.viewport :Viewport = viewport
        self.texture :Texture = texture
        self.direction = direction
        self.name = name

        # skill on left side
        self.attackBaseLocation = Coordinates(-1, 1)

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

        The location may depend on the parent, if it is not None
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
                self.coordinatesRel.x = parentLocation.x + (-1 * self.coordinates.x)
                + self.parent.texture.width - self.texture.width
                self.coordinatesRel.y = parentLocation.y + self.coordinates.y
            return self.coordinatesRel


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
        if (hitCoords.x >= self.coordinates.x
                and hitCoords.x < self.coordinates.x + self.texture.width
                and hitCoords.y >= self.coordinates.y
                and hitCoords.y < self.coordinates.y + self.texture.height):
            return True

        return False


    def getTextureHitCoordinates(self, animationIdx=0):
        # Only works on ActionTexture's
        locations = self.texture.getTextureHitCoordinates(animationIdx=0)
        baseLocation = self.getLocation()

        # make relative coordinates absolute
        for location in locations:
            location.x += baseLocation.x
            location.y += baseLocation.y

        return locations


    def getWeaponBaseLocation(self):
        # Slow
        loc = copy.copy(self.getLocation())

        loc.y -= 1
        if self.direction is Direction.left:
            loc.x -= -1
        else:
            loc.x += self.texture.width - 1

        return loc


    def getAttackBaseLocation(self):
        # Slow
        loc = copy.copy(self.getLocation())

        loc.y += self.attackBaseLocation.y
        if self.direction is Direction.left:
            loc.x += self.attackBaseLocation.x
        else:
            loc.x += self.texture.width - 1 - self.attackBaseLocation.x

        return loc


    def getAttackBaseLocationInverted(self):
        # Slow
        loc = copy.copy(self.getLocation())

        loc.y += self.attackBaseLocation.y
        if self.direction is Direction.right:
            loc.x += self.attackBaseLocation.x
        else:
            loc.x += self.texture.width - 1 - self.attackBaseLocation.x

        return loc


    def isOnScreen(self, wiggle :int =0):
        if (self.coordinates.x > self.viewport.getx() - wiggle
                and self.coordinates.x < self.viewport.getRightX() + wiggle):
            return True
        else:
            return False


    def isActive(self):
        return self.active


    def setActive(self, active):
        self.active = active


    def getDirection(self):
        return self.direction


    def setDirection(self, direction):
        self.direction = direction


    def setName(self, name):
        self.name = name


    def setZ(self, z):
        self.z = z
