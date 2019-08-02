#!/usr/bin/env python

import curses
import logging

from enum import Enum

from config import Config
from playeractionctrl import PlayerActionCtrl
from playerhit import PlayerHit
from playerstatus import PlayerStatus
from action import Action
from direction import Direction
from .figure import Figure

from sprite.speechsprite import SpeechSprite

logger = logging.getLogger(__name__)

class Player(Figure):
    def __init__(self, win, coordinates):
        Figure.__init__(self, win, coordinates)
        self.actionCtrl = PlayerActionCtrl(self)


    def getInput(self):
        key = self.win.getch()
        while key != -1:
            if key == ord(' '):
                self.actionCtrl.changeTo(Action.hitting, self.direction)
                self.playerHit.doHit(self.x, self.y, self.direction)

            if key == ord('q'):
                self.actionCtrl.changeTo(Action.shrugging, self.direction)

            if key == ord('w'):
                self.addSprite( SpeechSprite(None, parent=self) )

            if key == curses.KEY_LEFT:
                if self.x > 2:
                    self.x = self.x - 1
                    self.direction = Direction.left
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.actionCtrl.advanceStep()
            if key == curses.KEY_RIGHT: 
                if self.x < Config.columns - 4:
                    self.x = self.x + 1
                    self.direction = Direction.right
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.actionCtrl.advanceStep()
            if key == curses.KEY_UP: 
                if self.y > 2:
                    self.y = self.y - 1
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.actionCtrl.advanceStep()
            if key == curses.KEY_DOWN: 
                if self.y < Config.rows - 4:
                    self.y = self.y + 1
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.actionCtrl.advanceStep()

            key = self.win.getch()


    def ressurectMe(self): 
        if self.playerStatus.isAlive(): 
            return

        logger.info("P New player at: " + str(self.x) + " / " + str(self.y))
        self.playerStatus.init()
        self.actionCtrl.changeTo(Action.standing, None)