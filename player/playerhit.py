#!/usr/bin/env python

from sprite.sprite import Sprite
from action import Action
import logging

logger = logging.getLogger(__name__)

# Draws a "hit" at a specific location
# - Used to indicate where hit landed to the user
# - Used for collision detection
class PlayerHit(object):
    def __init__(self):
        self.duration = 30
        self.durationLeft = 30
        self.sprite = Sprite(Action.hit)
        self.x = 0
        self.y = 0
        self.isActive = False


    def doHit(self, x, y):
        # move hit to desired destination
        self.x = x + 4
        self.y = y + 1

        self.isActive = True
        self.durationLeft = self.duration
        self.sprite.initSprite(Action.hit)


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

