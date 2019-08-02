#!/usr/bin/env python

from sprite.phenomenasprite import PhenomenaSprite
from action import Action
from direction import Direction
import logging
from config import Config
from .entity import Entity

logger = logging.getLogger(__name__)

# Draws a "hit" at a specific location
# - Used to indicate where hit landed to the user
# - Used for collision detection
class CharacterWeapon(Entity):
    def __init__(self, win, parentCharacter):
        super(CharacterWeapon, self).__init__(win, parentCharacter, None)
        self.parentCharacter = parentCharacter
        self.sprite = PhenomenaSprite(action=Action.hit, parentEntity=self)

        # timeframe of this hit animation
        self.duration = Config.secToFrames(0.7)
        self.durationLeft = Config.secToFrames(0.7)

        # for drawing the hit, and see if the char is "hitting"
        self.isActive = False 

        # as we do collision detection later in the game loop, this item
        # may exists for multiple frames, and could therefore hit multiple
        # times. deactivate it after the first collision detection has been
        # performed
        self.collisionDetectionDone = False


    def doHit(self, x, y, direction):
        self.collisionDetectionDone = False
        self.isActive = True
        self.durationLeft = self.duration
        self.sprite.initSprite(Action.hit, direction, None)


    def isHitting(self): 
        return self.isActive


    def getHitCoordinates(self): 
        return self.getLocation()


    # we overwrite getLocation for now
    # should be fixed with mirroring implemented TODO
    def getLocation(self): 
        loc = self.parent.getLocation()

        if self.parent.direction is Direction.right: 
            loc['x'] += 3
            loc['y'] += 1
        else: 
            loc['x'] -= 1
            loc['y'] += 1

        return loc


