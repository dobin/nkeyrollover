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
        self.type = Action.standing
        self.sprite = PlayerSprite(self.type)
        self.isActive = True

        self.changeTo(Action.walking, Direction.left)


    def changeTo(self, action, direction):
        pass


    def specificAdvance(self): 
        pass


    # advance by step taken by the player
    def advanceStep(self):
        self.sprite.advanceStep()


    # advance by time
    def advance(self): 
        self.sprite.advance()
        self.durationLeft = self.durationLeft - 1
        self.specificAdvance()


    def draw(self, win, x, y):
        self.sprite.draw(win, x, y)

