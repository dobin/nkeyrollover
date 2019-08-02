#!/usr/bin/env python

import curses
import logging

from enum import Enum

from config import Config
from playeractionctrl import PlayerActionCtrl
from playerhit import PlayerHit
from playerstatus import PlayerStatus
from action import Action
from direction import Direction
from .entity import Entity

from sprite.speechsprite import SpeechSprite

logger = logging.getLogger(__name__)

class Figure(Entity):
    def __init__(self, win, parent, coordinates):
        super(Figure, self).__init__(win, parent, coordinates)
        
        self.playerStatus = PlayerStatus()
        self.playerHit = PlayerHit(win=win, parentFigure=self)
        self.aSprite = None
        self.actionCtrl = None # filled in children


    def getInput(self, playerLocation): 
        pass


    def ressurectMe(self): 
        pass


    def draw(self):
        super(Figure, self).draw(self.win)
        self.playerHit.draw(self.win)

        if self.aSprite is not None: 
            self.aSprite.draw(self.win)


    def advance(self):
        super(Figure, self).advance()
        self.actionCtrl.advance()
        self.playerHit.advance()
        self.playerStatus.advance()

        if self.aSprite is not None: 
            self.aSprite.advance()


    def getHit(self, damage):
        self.playerStatus.getHit(damage)
        if not self.playerStatus.isAlive():
            self.actionCtrl.changeTo(Action.dying, None)


    def addSprite(self, sprite): 
        self.aSprite = sprite


    def collidesWithPoint(self, hitCoords):
        if hitCoords['x'] >= self.x and hitCoords['x'] <= self.x + 3:
            if hitCoords['y'] >= self.y and hitCoords['y'] <= self.y + 3:
                return True

        return False

