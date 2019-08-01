#!/usr/bin/env python

from sprite.playersprite import PlayerSprite
from action import Action
from direction import Direction
from config import Config
import logging

logger = logging.getLogger(__name__)


class PlayerAction(object):
    def __init__(self):
        self.duration = 0
        self.durationLeft = 0
        self.type = Action.standing
        self.sprite = PlayerSprite(self.type)


    def changeTo(self, action, direction):
        if action is Action.walking:
            # we start, or continue, walking
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)

            # if we were already walking, dont destroy the animation state
            if self.type is not Action.walking:
                self.sprite.initSprite(action, direction)
        else: 
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)

            self.sprite.initSprite(action, direction)

        self.type = action


    # advance by step taken by the player
    def advanceStep(self):
        self.sprite.advanceStep()


    # advance by time
    def advance(self): 
        self.sprite.advance()

        self.durationLeft = self.durationLeft - 1

        # stand still after some non walking
        if self.type is Action.walking: 
            if self.durationLeft == 0:
                self.type = Action.standing
                self.sprite.initSprite(Action.standing, Direction.right)

        # after hitting is finished, stand still
        if self.type is Action.hitting: 
            if self.durationLeft == 0:
                self.type = Action.standing
                self.sprite.initSprite(Action.standing, Direction.right)



    def draw(self, win, x, y):
        self.sprite.draw(win, x, y)

