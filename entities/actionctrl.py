#!/usr/bin/env python

from sprite.charactersprite import CharacterSprite
from .direction import Direction
from config import Config
from utilities.timer import Timer
import logging

logger = logging.getLogger(__name__)


class ActionCtrl(object):
    def __init__(self, parentEntity, world):
        self.world = world
        self.parentEntity = parentEntity
        
        # timer which are used individually for each action
        self.durationTimer = Timer(0.0)


    # change to another action
    # implemented by children
    def changeTo(self, newAction, direction):
        raise NotImplementedError('subclasses must override this abstract method')


    # advance by time
    def advance(self, deltaTime): 
        self.durationTimer.advance(deltaTime)

        # defined by children
        self.specificAdvance()


    def specificAdvance(self): 
        raise NotImplementedError('subclasses must override this abstract method')

