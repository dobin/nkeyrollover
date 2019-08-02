#!/usr/bin/env python

from sprite.playersprite import PlayerSprite
from action import Action
from direction import Direction
from config import Config
import logging

logger = logging.getLogger(__name__)


class BaseAction(object):
    def __init__(self):
        self.duration = 0
        self.durationLeft = 0
        
        # the sprite beloging to this action
        self.sprite = PlayerSprite(None)

        # the director will remove figure from the Alive list if this is false
        # making us unrenderable, and unadvancable (aka when truly dead)
        self.isActive = True

        # init a sane one
        self.type = Action.standing
        self.changeTo(Action.walking, Direction.left)


    # change to another action
    # implemented by children
    def changeTo(self, newAction, direction):
        pass


    # advance, step taken by the player via input
    def advanceStep(self):
        self.sprite.advanceStep()


    # advance by time
    def advance(self): 
        self.sprite.advance()
        self.durationLeft = self.durationLeft - 1
        self.specificAdvance()

    
    # implemented by children
    def specificAdvance(self): 
        pass


    def draw(self, win, x, y):
        self.sprite.draw(win, x, y)
