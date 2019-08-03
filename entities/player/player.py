#!/usr/bin/env python

import curses
import logging

from enum import Enum

from config import Config
from .playeractionctrl import PlayerActionCtrl
from entities.characterweapon import CharacterWeapon
from entities.characterstatus import CharacterStatus
from entities.action import Action
from entities.direction import Direction
from entities.character import Character

from sprite.speechsprite import SpeechSprite
from sprite.charactersprite import CharacterSprite


logger = logging.getLogger(__name__)

class Player(Character):
    def __init__(self, win, parent, spawnBoundaries, world):
        Character.__init__(self, win, parent, spawnBoundaries, world)
        self.actionCtrl = PlayerActionCtrl(parentEntity=self, world=world)
        self.sprite = CharacterSprite(parentEntity=self)

        # first action is standing around
        self.actionCtrl.changeTo(Action.walking, Direction.left)

        self.x = 10
        self.y = 10


    def getInput(self):
        key = self.win.getch()
        while key != -1:
            if key == ord(' '):
                self.actionCtrl.changeTo(Action.hitting, self.direction)
                self.characterWeapon.doHit()

            if key == ord('q'):
                self.actionCtrl.changeTo(Action.shrugging, self.direction)

            if key == ord('w'):
                self.addSprite( SpeechSprite(None, parentEntity=self) )

            if key == curses.KEY_LEFT:
                if self.x > 1:
                    self.x = self.x - 1
                    self.direction = Direction.left
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.advanceStep()
            if key == curses.KEY_RIGHT: 
                if self.x < Config.columns - self.sprite.width - 1:
                    self.x = self.x + 1
                    self.direction = Direction.right
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.advanceStep()
            if key == curses.KEY_UP: 
                if self.y > 2:
                    self.y = self.y - 1
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.advanceStep()
            if key == curses.KEY_DOWN: 
                if self.y < Config.rows - self.sprite.height - 1:
                    self.y = self.y + 1
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.advanceStep()

            key = self.win.getch()


    def advance(self, deltaTime):
        super(Player, self).advance(deltaTime) # advance Character part (duration, sprite)
        self.actionCtrl.advance(deltaTime) # advance actions (duration, Action transfers)


    def ressurectMe(self): 
        if self.characterStatus.isAlive(): 
            return

        logger.info("P New player at: " + str(self.x) + " / " + str(self.y))
        self.characterStatus.init()
        self.actionCtrl.changeTo(Action.standing, None)

        
