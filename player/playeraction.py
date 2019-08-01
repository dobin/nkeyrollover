#!/usr/bin/env python

from sprite.sprite import Sprite
from action import Action


class PlayerAction(object):
    def __init__(self):
        self.duration = 0
        self.durationLeft = 0
        self.type = Action.standing
        self.sprite = Sprite(self.type)


    def changeTo(self, action):
        self.type = action
        self.duration = 50
        self.durationLeft = 50
        self.sprite = Sprite(self.type)

    def advance(self): 
        self.sprite.advance()

    def draw(self, win, x, y):
        self.sprite.draw(win, x, y)

