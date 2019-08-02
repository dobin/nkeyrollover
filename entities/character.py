#!/usr/bin/env python

import curses
import logging

from enum import Enum

from config import Config
from entities.player.playeractionctrl import PlayerActionCtrl
from characterweapon import CharacterWeapon
from characterstatus import CharacterStatus
from action import Action
from direction import Direction
from entities.entity import Entity

from sprite.speechsprite import SpeechSprite

logger = logging.getLogger(__name__)

class Character(Entity):
    """ A character is either a player or an enemy"""

    def __init__(self, win, parent, coordinates):
        super(Character, self).__init__(win, parent, coordinates)
        
        self.characterStatus = CharacterStatus()
        self.characterWeapon = CharacterWeapon(win=win, parentCharacter=self)
        self.aSprite = None
        self.actionCtrl = None # filled in children


    def getInput(self, playerLocation): 
        raise NotImplementedError('subclasses must override this abstract method')


    def ressurectMe(self): 
        raise NotImplementedError('subclasses must override this abstract method')


    def draw(self):
        super(Character, self).draw(self.win)
        self.characterWeapon.draw(self.win)

        if self.aSprite is not None: 
            self.aSprite.draw(self.win)


    def advance(self):
        super(Character, self).advance() # advance Entity part (duration, sprite)
        self.actionCtrl.advance() # advance actions (duration, Action transfers)
        self.characterWeapon.advance() # update weapon (duration, sprite)
        self.characterStatus.advance() # update health, mana etc.

        if self.aSprite is not None: # update additional sprites, if any
            self.aSprite.advance()


    def getHit(self, damage):
        self.characterStatus.getHit(damage)
        if not self.characterStatus.isAlive():
            self.actionCtrl.changeTo(Action.dying, None)


    def addSprite(self, sprite): 
        self.aSprite = sprite
