#!/usr/bin/env python

from sprite.playersprite import PlayerSprite
from action import Action
from direction import Direction
import logging
from config import Config

logger = logging.getLogger(__name__)

# Draws a "hit" at a specific location
# - Used to indicate where hit landed to the user
# - Used for collision detection
class PlayerHit(object):
    def __init__(self):
        self.duration = Config.secToFrames(0.7)
        self.durationLeft = Config.secToFrames(0.7)
        self.sprite = PlayerSprite(Action.hit)
        self.x = 0
        self.y = 0

        # for drawing the hit, and see if the char is "hitting"
        self.isActive = False 


    def doHit(self, x, y, direction):
        # move hit to desired destination
        if direction is Direction.right:
            self.x = x + 3
            self.y = y + 1
        else:
            self.x = x - 1
            self.y = y + 1

        self.isActive = True
        self.durationLeft = self.duration
        self.sprite.initSprite(Action.hit, direction)


    def isHitting(self): 
        return self.isActive


    def getHitCoordinates(self): 
        return { 'x': self.x, 'y': self.y }


    def advance(self):
        if not self.isActive: 
            return 

        self.sprite.advance()
        self.durationLeft = self.durationLeft - 1
        if self.durationLeft == 0:
            self.isActive = False


    def draw(self, win):
        if self.isActive:
            self.sprite.draw(win, self.x, self.y)

