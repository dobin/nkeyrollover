#!/usr/bin/env python

import logging

from config import Config
from sprite.phenomenasprite import PhenomenaSprite
from .direction import Direction
from .entity import Entity
from .entitytype import EntityType
from texture.phenomenatype import PhenomenaType
from utilities.timer import Timer

logger = logging.getLogger(__name__)


# Draws a "hit" at a specific location
# - Used to indicate where hit landed to the user
# - Used for collision detection
class CharacterWeapon(Entity):
    def __init__(self, win, parentCharacter):
        super(CharacterWeapon, self).__init__(win, parentCharacter, EntityType.weapon)
        self.sprite = PhenomenaSprite(phenomenaType=PhenomenaType.hit, parentEntity=self)

        # the duration of the hitting animation
        self.durationTimer.setTimer( self.sprite.getAnimationTime() )
        self.durationTimer.reset()

        # cooldown. 0.2 is actually lower than whats possible, even with 100fps
        self.cooldownTimer = Timer(0.2, instant=True)

        # for drawing the hit, and see if the char is "hitting"
        self.isActive = False 


    def advance(self, deltaTime):
        super(CharacterWeapon, self).advance(deltaTime)
        self.cooldownTimer.advance(deltaTime)


    def doHit(self): 
        raise NotImplementedError('subclasses must override this abstract method')


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


