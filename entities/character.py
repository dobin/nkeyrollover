#!/usr/bin/env python

import random
import curses
import logging

from enum import Enum

from config import Config
from entities.player.playeractionctrl import PlayerActionCtrl
from entities.entity import Entity
from .characterstatus import CharacterStatus
from .direction import Direction
from sprite.speechsprite import SpeechSprite

logger = logging.getLogger(__name__)

class Character(Entity):
    """ A character is either a player or an enemy"""

    def __init__(self, win, parentEntity, spawnBoundaries, world, entityType):
        super(Character, self).__init__(win, parentEntity, entityType)
        self.world = world
        self.spawnBoundaries = spawnBoundaries

        self.characterStatus = CharacterStatus()
        self.speechSprite = SpeechSprite(parentEntity=self, displayText='')
        self.speechSprite.setActive(False)
        self.characterAttack = None # by children
        self.actionCtrl = None # filled in children
        self.characterInfo = None # filled by children


    def getInput(self, playerLocation): 
        raise NotImplementedError('subclasses must override this abstract method')


    def gmRessurectMe(self): 
        raise NotImplementedError('subclasses must override this abstract method')


    def gmHandleHit(self, damage):
        raise NotImplementedError('subclasses must override this abstract method')


    def draw(self):
        super(Character, self).draw(self.win)
        self.speechSprite.draw(self.win)


    def drawCharacterAttack(self): 
        self.characterAttack.draw(self.win)


    def advance(self, deltaTime):
        super(Character, self).advance(deltaTime) # advance Entity part (duration, sprite)

        self.characterAttack.advance(deltaTime) # update weapon (duration, sprite)
        self.characterStatus.advance(deltaTime) # update health, mana etc.
        self.speechSprite.advance(deltaTime)


    def getRandomHead(self):
        return random.choice([ '^', 'o', 'O', 'v', 'V'])


    def getRandomBody(self): 
        return random.choice([ 'X', 'o', 'O', 'v', 'V'])