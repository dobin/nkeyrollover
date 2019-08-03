#!/usr/bin/env python

from sprite.charactersprite import CharacterSprite
from .action import Action
from .direction import Direction
from config import Config
import logging

logger = logging.getLogger(__name__)


class ActionCtrl(object):
    def __init__(self, parentEntity, world):
        self.world = world
        self.parentEntity = parentEntity
        
        # timer which are used individually for each action
        self.duration = 0
        self.durationLeft = 0
        
        # We are new
        self.action = Action.spawning


    def getAction(self): 
        return self.action
        

    # change to another action
    # implemented by children
    def changeTo(self, newAction, direction):
        raise NotImplementedError('subclasses must override this abstract method')


    def resetDuration(self, duration, durationLeft):
        self.duration = duration
        self.durationLeft = durationLeft


    def durationTimeIsUp(self): 
        if self.durationLeft <= 0:
            return True
        else: 
            return False


    # advance by time
    def advance(self): 
        self.durationLeft = self.durationLeft - 1

        # defined by children
        self.specificAdvance()


    def specificAdvance(self): 
        raise NotImplementedError('subclasses must override this abstract method')

