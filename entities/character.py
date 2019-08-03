#!/usr/bin/env python

import curses
import logging

from enum import Enum

from config import Config
from entities.player.playeractionctrl import PlayerActionCtrl
from entities.entity import Entity
from .characterweapon import CharacterWeapon
from .characterstatus import CharacterStatus
from .action import Action
from .direction import Direction
from sprite.speechsprite import SpeechSprite

logger = logging.getLogger(__name__)

class Character(Entity):
    """ A character is either a player or an enemy"""

    def __init__(self, win, parent, spawnBoundaries, world):
        super(Character, self).__init__(win, parent)
        self.world = world
        self.spawnBoundaries = spawnBoundaries

        self.characterStatus = CharacterStatus()
        self.characterWeapon = CharacterWeapon(win=win, parentCharacter=self)
        self.aSprite = None
        self.actionCtrl = None # filled in children


    def getInput(self, playerLocation): 
        raise NotImplementedError('subclasses must override this abstract method')


    def gmRessurectMe(self): 
        raise NotImplementedError('subclasses must override this abstract method')


    def gmHandleHit(self, damage):
        raise NotImplementedError('subclasses must override this abstract method')


    def draw(self):
        super(Character, self).draw(self.win)
        self.characterWeapon.draw(self.win)

        if self.aSprite is not None: 
            self.aSprite.draw(self.win)


    def advance(self, deltaTime):
        super(Character, self).advance(deltaTime) # advance Entity part (duration, sprite)

        self.characterWeapon.advance(deltaTime) # update weapon (duration, sprite)
        self.characterStatus.advance(deltaTime) # update health, mana etc.

        if self.aSprite is not None: # update additional sprites, if any
            self.aSprite.advance(deltaTime)


    def addSprite(self, sprite): 
        self.aSprite = sprite
