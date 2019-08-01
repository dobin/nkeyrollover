#!/usr/bin/env python

import curses
import logging

from enum import Enum

from playeraction import PlayerAction
from playerhit import PlayerHit
from action import Action


from sprite.sprite import Sprite

logger = logging.getLogger(__name__)


class Looking(Enum): 
    left = 0
    right = 1


class Player(object):
    def __init__(self, win):
        self.x = 10
        self.y = 10
        self.win = win
        self.looking = Looking.right
        
        self.playerAction = PlayerAction()
        self.playerHit = PlayerHit()
        

    def draw(self):
        self.playerAction.draw(self.win, self.x, self.y)

        self.playerHit.draw(self.win)


    def advance(self): 
        self.playerAction.advance()

        self.playerHit.advance()


    def getInput(self):
        key = self.win.getch()

        if key == ord(' '):
            self.playerAction.changeTo(Action.hitting)
            self.playerHit.doHit(self.x, self.y)

        if key == ord('q'):
            self.playerAction.changeTo(Action.shrugging)


        if key == curses.KEY_LEFT: 
            self.x = self.x - 1
            self.looking = Looking.left
            self.playerAction.changeTo(Action.walking)
        if key == curses.KEY_RIGHT: 
            self.x = self.x + 1
            self.looking = Looking.right
            self.playerAction.changeTo(Action.walking)
        if key == curses.KEY_UP: 
            self.y = self.y - 1
            self.playerAction.changeTo(Action.walking)
        if key == curses.KEY_DOWN: 
            self.y = self.y + 1
            self.playerAction.changeTo(Action.walking)