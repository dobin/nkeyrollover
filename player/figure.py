#!/usr/bin/env python

import curses
import logging

from enum import Enum

from config import Config
from playeraction import PlayerAction
from playerhit import PlayerHit
from playerstatus import PlayerStatus
from action import Action
from direction import Direction

from sprite.speechsprite import SpeechSprite

logger = logging.getLogger(__name__)

class Figure(object):
    def __init__(self, win, coordinates):
        self.x = 10
        self.y = 10
        self.win = win
        self.direction = Direction.right
        
        self.playerStatus = PlayerStatus()
        self.playerHit = PlayerHit()
        self.aSprite = None
        self.playerAction = None # filled in children


    def getInput(self, playerLocation): 
        pass


    def ressurectMe(self): 
        pass


    def draw(self):
        self.playerAction.draw(self.win, self.x, self.y)
        self.playerHit.draw(self.win)

        if self.aSprite is not None: 
            self.aSprite.draw(self.win, self.x, self.y)


    def advance(self): 
        self.playerAction.advance()
        self.playerHit.advance()
        self.playerStatus.advance()

        if self.aSprite is not None: 
            self.aSprite.advance()


    def getHit(self, damage):
        self.playerStatus.getHit(damage)
        if not self.playerStatus.isAlive():
            self.playerAction.changeTo(Action.dying, None)


    def addSprite(self, sprite): 
        self.aSprite = sprite


    def collidesWithPoint(self, hitCoords):
        if hitCoords['x'] >= self.x and hitCoords['x'] <= self.x + 3:
            if hitCoords['y'] >= self.y and hitCoords['y'] <= self.y + 3:
                return True

        return False


    def getLocation(self): 
        loc = {
            'x': self.x,
            'y': self.y,
        }
        return loc            