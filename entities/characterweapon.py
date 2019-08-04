#!/usr/bin/env python

import logging

from config import Config
from sprite.phenomenasprite import PhenomenaSprite
from .direction import Direction
from .entity import Entity
from .entitytype import EntityType
from texture.phenomenatype import PhenomenaType

logger = logging.getLogger(__name__)


# Draws a "hit" at a specific location
# - Used to indicate where hit landed to the user
# - Used for collision detection
class CharacterWeapon(Entity):
    def __init__(self, win, parentCharacter):
        super(CharacterWeapon, self).__init__(win, parentCharacter, EntityType.weapon)
        self.sprite = PhenomenaSprite(phenomenaType=PhenomenaType.hit, parentEntity=self)
        self.reset()

    
    def reset(self):
        # timeframe of this hit animation
        self.durationTimer.setTimer(0.7)
        self.durationTimer.reset()

        # for drawing the hit, and see if the char is "hitting"
        self.isActive = False 


    def doHit(self): 
        raise NotImplementedError('subclasses must override this abstract method')


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


