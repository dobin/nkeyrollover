#!/usr/bin/env python

from sprite.phenomenasprite import PhenomenaSprite
from .action import Action
from .direction import Direction
import logging
from config import Config
from .entity import Entity

logger = logging.getLogger(__name__)

# Draws a "hit" at a specific location
# - Used to indicate where hit landed to the user
# - Used for collision detection
class CharacterWeapon(Entity):
    def __init__(self, win, parentCharacter):
        super(CharacterWeapon, self).__init__(win, parentCharacter)
        self.sprite = PhenomenaSprite(action=Action.hit, parentEntity=self)
        self.reset()

    
    def reset(self):
        # timeframe of this hit animation
        self.durationTimer.setTimer(0.7)
        self.durationTimer.reset()

        # for drawing the hit, and see if the char is "hitting"
        self.isActive = False 


    def doHit(self):
        hittedEnemies = self.parent.world.director.getEnemiesHit(self.getLocation())
        for enemy in hittedEnemies: 
            enemy.gmHandleHit(50)

        self.isActive = True
        self.durationTimer.reset()
        self.sprite.initSprite(Action.hit, self.parent.direction, None)


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


