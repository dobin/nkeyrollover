#!/usr/bin/env python

import random
import curses
import logging
from enum import Enum
import copy

from config import Config
from entities.entity import Entity
from .characterstatus import CharacterStatus
from sprite.direction import Direction
from world.viewport import Viewport

logger = logging.getLogger(__name__)


class Character(object):
    """ A character is either a player or an enemy"""

    def __init__(
        self, viewport :Viewport, parent,
        world, entityType :Entity
    ):
        self.parent = parent
        self.entityType = entityType
        self.world = world

        self.characterStatus = CharacterStatus()
        self.speechTexture = SpeechTexture(parentSprite=self, displayText='')
        self.speechTexture.setActive(False)
        self.characterInfo = None # filled by children


    def getInput(self, playerLocation):
        raise NotImplementedError('subclasses must override this abstract method')


    def gmRessurectMe(self):
        raise NotImplementedError('subclasses must override this abstract method')


    def gmHandleHit(self, damage):
        raise NotImplementedError('subclasses must override this abstract method')


    def move(self, x=None, y=None):
        raise NotImplementedError('subclasses must override this abstract method')


    def draw(self):
        #super(Character, self).draw()
        self.speechTexture.draw(self.viewport)


    def advance(self, deltaTime):
        #super(Character, self).advance(deltaTime) # advance Entity part (duration, sprite)

        self.characterStatus.advance(deltaTime) # update health, mana etc.
        self.speechTexture.advance(deltaTime)


    def getRandomHead(self):
        return random.choice([ '^', 'o', 'O', 'v', 'V'])


    def getRandomBody(self):
        return random.choice([ 'X', 'o', 'O', 'v', 'V', 'M', 'm' ])

