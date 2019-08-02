#!/usr/bin/env python

from sprite.charactersprite import CharacterSprite
from action import Action
from direction import Direction
from config import Config
import logging

logger = logging.getLogger(__name__)


class BaseActionCtrl(object):
    def __init__(self, parentEntity):
        self.duration = 0
        self.durationLeft = 0
        
        self.parentEntity = parentEntity

        # We are new
        self.type = Action.spawning


    # change to another action
    # implemented by children
    def changeTo(self, newAction, direction):
        pass


    # advance by time
    def advance(self): 
        self.durationLeft = self.durationLeft - 1
        self.specificAdvance()

    
    # implemented by children
    def specificAdvance(self): 
        pass
