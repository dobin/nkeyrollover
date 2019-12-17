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
from messaging import messaging, MessageType
from utilities.color import Color
from system.graphics.particleeffecttype import ParticleEffectType
from utilities.utilities import Utility

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
        name='',
        canMoveOutsideMap=True
    ):
        self.viewport :Viewport = viewport
        self.texture :Texture = texture
        self.direction = direction
        self.name = name

        # coordinates are based on left side orientation of renderable
        self.attackBaseLocation = Coordinates(-1, 1)
        self.weaponBaseLocation = Coordinates(0, -1)

        self.storedCoordinates = Coordinates()

        # if parent is given, this position will always be relative
        # to that parent
        self.parent :Renderable = parent

        # some things, like weapon, need to be on the correct
        # side of the parent
        self.useParentDirection = useParentDirection

        # if this is being rendered
        self.active :bool = active

        self.canMoveOutsideMap = canMoveOutsideMap

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


    def getLocationTopCenter(self):
        # slow, but its currently only used by rare events like skillExplosion
        loc = copy.copy(self.getLocation())
        # this will round down
        loc.x += int(self.texture.width / 2)
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


    def getHitLocationsOf(self, hitLocations :List[Coordinates]):
        locations = []
        for hitLocation in hitLocations:
            if self.collidesWithPoint(hitLocation):
                locations.append(hitLocation)

        return locations


    def collidesWithPoint(self, hitCoords :Coordinates):
        """
        Returns true if the 1x1 particle at hitCoords hits a nonempty part of
        this renderable's texture
        """

        logging.debug("Hit: {}/{}  Renderable: {}/{} W: {} H: {}".format(
            hitCoords.x, hitCoords.y,
            self.coordinates.x, self.coordinates.y,
            self.texture.height, self.texture.width
        ))
        # broad check
        if (hitCoords.x >= self.coordinates.x
                and hitCoords.x < self.coordinates.x + self.texture.width
                and hitCoords.y >= self.coordinates.y
                and hitCoords.y < self.coordinates.y + self.texture.height):

            # precise check
            currentFrame = self.texture.getCurrentFrame()
            xOff = hitCoords.x - self.coordinates.x
            yOff = hitCoords.y - self.coordinates.y

            if yOff >= len(currentFrame):
                logging.error("CollideWithPoint error: {} {}".format(
                    yOff, len(currentFrame)
                ))
                return False
            if xOff >= len(currentFrame[yOff]):
                logging.error("CollideWithPoint error: {} {}".format(
                    xOff, len(currentFrame[yOff])
                ))
                return False

            if currentFrame[yOff][xOff] != '':
                return True

        return False


    def overlapsWith(self, renderable):
        """
        Returns true if the renderable overlaps with this current renderables texture
        Fast but unexact.
        """
        if self.coordinates.x + self.texture.width > renderable.coordinates.x:
            if self.coordinates.x < renderable.coordinates.x + renderable.texture.width:
                if self.coordinates.y < renderable.coordinates.y + renderable.texture.height:
                    if self.coordinates.y + self.texture.height > renderable.coordinates.y:
                        return True

        return False


    def overlapsWithRenderablePixel(self, renderable):
        # if not self.overlapsWithCoordinates(renderable.getLocationAndSize()):
        #     return False

        meTextureArr = self.texture.getCurrentFrame()
        heTextureArr = renderable.texture.getCurrentFrame()

        meRenderable = self
        heRenderable = renderable

        left = max(meRenderable.coordinates.x, heRenderable.coordinates.x)
        right = min(
            meRenderable.coordinates.x + meRenderable.texture.width,
            heRenderable.coordinates.x + heRenderable.texture.width)
        me_left = left - meRenderable.coordinates.x
        me_right = right - meRenderable.coordinates.x

        top = max(meRenderable.coordinates.y, heRenderable.coordinates.y)
        bottom = min(
            meRenderable.coordinates.y + meRenderable.texture.height,
            heRenderable.coordinates.y + heRenderable.texture.height)
        me_top = top - meRenderable.coordinates.y
        me_bottom = bottom - meRenderable.coordinates.y

        y = me_top
        while y < me_bottom:
            x = me_left
            while x < me_right:
                # Sometimes crash here. lets log it for now
                # Make non-overlapping on error for now
                if y > len(meTextureArr):
                    logging.exception("Coordinate does not exist: Y: {}  Len: {} -  {} and {}".format(
                        y, len(meTextureArr), 
                        renderable, self
                    ))
                    return False
                if x > len(meTextureArr[y]):
                    logging.exception("Coordinate does not exist: X: {}  Len: {} - {} and {}".format(
                        xxx, len(meTextureArr[y]),
                        renderable, self
                    ))
                    return False
                myc = meTextureArr[y][x]
                xxx, yyy = Utility.getOffsetFor(self, renderable, x, y)
                
                # Sometimes crash here. lets log it for now
                # Make non-overlapping on error for now
                if yyy > len(heTextureArr):
                    logging.exception("Coordinate does not exist: Y: {}  Len: {} -  {} and {}".format(
                        yyy, len(heTextureArr),
                        renderable, self
                    ))
                    return False
                if xxx > len(heTextureArr[yyy]):
                    logging.exception("Coordinate does not exist: X: {}  Len: {} -  {} and {}".format(
                        xxx, len(heTextureArr[yyy]),
                        renderable, self
                    ))
                    return False

                hisc = heTextureArr[yyy][xxx]

                if myc != '' and hisc != '':
                    return True

                x += 1
            y += 1

        return False


    def overlapsWithPointPixel(self, x, y):
        meTextureArr = self.texture.getCurrentFrame()

        meX = x - self.coordinates.x
        meY = y - self.coordinates.y

        if meTextureArr[meY][meX] != '':
            return True

        return False


    def distanceToBorder(self, renderable):
        """Distance from my border to the border of extCoords.

        If renderables are adjectant, distance is 0.
        """
        if self.coordinates.x < renderable.coordinates.x:
            # Me   Extcoords
            distX = renderable.coordinates.x - (self.coordinates.x + self.texture.width)
        elif self.coordinates.x > renderable.coordinates.x:
            # Extcoords   Me
            distX = self.coordinates.x - (renderable.coordinates.x + renderable.texture.width)
        else:
            # Extcoords
            # Me
            distX = 0

        # Me
        # Extcoords
        if self.coordinates.y < renderable.coordinates.y:
            distY = renderable.coordinates.y - (self.coordinates.y + self.texture.height)
        elif self.coordinates.y > renderable.coordinates.y:
            distY = self.coordinates.y - (renderable.coordinates.y + renderable.texture.height)
        else:
            distY = 0

        res = {
            'x': distX,
            'y': distY,
            'sum': distX + distY
        }

        return res


    def distanceToPoint(self, x, y):
        x = abs(self.coordinates.x - x)
        y = abs(self.coordinates.y - y)
        return x + y


    def getAttackBaseLocation(self):
        """
        Used to:
        - As Enemy/AI: Check distance, direction to player (chase). Bigger enemies
          basically define their feet as base, so they align with the player better.
        """

        # Slow
        loc = copy.copy(self.getLocation())

        loc.y += self.attackBaseLocation.y
        if self.direction is Direction.left:
            loc.x += self.attackBaseLocation.x
        else:
            loc.x += (self.texture.width - 1 - self.attackBaseLocation.x)

        return loc


    def getAttackBaseLocationInverted(self):
        # Slow
        loc = copy.copy(self.getLocation())

        loc.y += self.attackBaseLocation.y
        if self.direction is Direction.right:
            loc.x += self.attackBaseLocation.x
        else:
            loc.x += (self.texture.width - 1 - self.attackBaseLocation.x)

        return loc


    def isOnScreen(self, wiggle :int =0):
        if (self.coordinates.x + self.texture.width > self.viewport.getx() - wiggle
                and self.coordinates.x < self.viewport.getRightX() + wiggle):
            return True
        else:
            return False


    def storeCoords(self):
        self.storedCoordinates.x = self.coordinates.x
        self.storedCoordinates.y = self.coordinates.y


    def restoreCoords(self):
        self.coordinates.x = self.storedCoordinates.x
        self.coordinates.y = self.storedCoordinates.y


    def changeLocationFromStored(self, x, y):
        self.coordinates.x = self.storedCoordinates.x + x
        self.coordinates.y = self.storedCoordinates.y + y


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
