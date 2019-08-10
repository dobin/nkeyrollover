#!/usr/bin/env python

import random
import curses
import logging
from enum import Enum

from config import Config
from entities.entity import Entity
from .characterstatus import CharacterStatus
from sprite.direction import Direction
from texture.speechtexture import SpeechTexture

logger = logging.getLogger(__name__)


class Character(Entity):
    """ A character is either a player or an enemy"""

    def __init__(self, viewport, parentEntity, spawnBoundaries, world, entityType):
        super(Character, self).__init__(viewport, parentEntity, entityType)
        self.world = world
        self.spawnBoundaries = spawnBoundaries

        self.characterStatus = CharacterStatus()
        self.speechTexture = SpeechTexture(parentSprite=self, displayText='')
        self.speechTexture.setActive(False)
        self.characterAttack = None # by children
        self.characterInfo = None # filled by children


    def getInput(self, playerLocation): 
        raise NotImplementedError('subclasses must override this abstract method')


    def gmHandleEnemyHit(self, damage, isAttack=True): 
        self.characterStatus.enemyHit(damage, isAttack)


    def gmRessurectMe(self): 
        raise NotImplementedError('subclasses must override this abstract method')


    def gmHandleHit(self, damage):
        raise NotImplementedError('subclasses must override this abstract method')


    def draw(self):
        super(Character, self).draw()
        self.speechTexture.draw(self.viewport)


    def drawCharacterAttack(self): 
        self.characterAttack.draw()


    def advance(self, deltaTime):
        super(Character, self).advance(deltaTime) # advance Entity part (duration, sprite)

        self.characterAttack.advance(deltaTime) # update weapon (duration, sprite)
        self.characterStatus.advance(deltaTime) # update health, mana etc.
        self.speechTexture.advance(deltaTime)


    def getRandomHead(self):
        return random.choice([ '^', 'o', 'O', 'v', 'V'])


    def getRandomBody(self): 
        return random.choice([ 'X', 'o', 'O', 'v', 'V'])

    
    def getLocationCenter(self): 
        loc = self.getLocation()
        loc.x += 1
        loc.y += 1
        return loc