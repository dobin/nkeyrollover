#!/usr/bin/env python

import curses
import logging

from enum import Enum

from playeraction import PlayerAction
from playerhit import PlayerHit
from action import Action
from direction import Direction

from sprite.speechsprite import SpeechSprite

logger = logging.getLogger(__name__)

class Player(object):
    def __init__(self, win):
        self.x = 10
        self.y = 10
        self.win = win
        self.direction = Direction.right
        
        self.playerAction = PlayerAction()
        self.playerHit = PlayerHit()
        self.aSprite = None
        

    def draw(self):
        self.playerAction.draw(self.win, self.x, self.y)
        self.playerHit.draw(self.win)

        if self.aSprite is not None: 
            self.aSprite.draw(self.win, self.x, self.y)


    def advance(self): 
        self.playerAction.advance()
        self.playerHit.advance()

        if self.aSprite is not None: 
            self.aSprite.advance()


    def getInput(self):
        key = self.win.getch()

        if key == ord(' '):
            self.playerAction.changeTo(Action.hitting, self.direction)
            self.playerHit.doHit(self.x, self.y, self.direction)

        if key == ord('q'):
            self.playerAction.changeTo(Action.shrugging, self.direction)

        if key == ord('w'):
            self.addSprite( SpeechSprite(None) )

        if key == curses.KEY_LEFT: 
            self.x = self.x - 1
            self.direction = Direction.left
            self.playerAction.changeTo(Action.walking, self.direction)
            self.playerAction.advanceStep()
        if key == curses.KEY_RIGHT: 
            self.x = self.x + 1
            self.direction = Direction.right
            self.playerAction.changeTo(Action.walking, self.direction)
            self.playerAction.advanceStep()
        if key == curses.KEY_UP: 
            self.y = self.y - 1
            self.playerAction.changeTo(Action.walking, self.direction)
            self.playerAction.advanceStep()
        if key == curses.KEY_DOWN: 
            self.y = self.y + 1
            self.playerAction.changeTo(Action.walking, self.direction)
            self.playerAction.advanceStep()


    def addSprite(self, sprite): 
        self.aSprite = sprite


    def collidesWithPoint(self, hitCoords):
        if hitCoords['x'] >= self.x and hitCoords['x'] <= self.x + 3:
            if hitCoords['y'] >= self.y and hitCoords['y'] <= self.y + 3:
                return True

        return False