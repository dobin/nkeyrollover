#!/usr/bin/env python

import curses
import logging

from enum import Enum

from utilities.utilities import Utility
from config import Config
from .playeractionctrl import PlayerActionCtrl
from .playerweapon import PlayerWeapon
from entities.characterstatus import CharacterStatus
from entities.action import Action
from entities.direction import Direction
from entities.character import Character
from entities.entitytype import EntityType
from sprite.speechsprite import SpeechSprite
from sprite.charactersprite import CharacterSprite


logger = logging.getLogger(__name__)

class Player(Character):
    def __init__(self, win, parent, spawnBoundaries, world):
        Character.__init__(self, win, parent, spawnBoundaries, world, EntityType.player)
        self.actionCtrl = PlayerActionCtrl(parentEntity=self, world=world)
        self.sprite = CharacterSprite(parentEntity=self)
        self.characterWeapon = PlayerWeapon(win=win, parentCharacter=self)

        # first action is standing around
        self.actionCtrl.changeTo(Action.standing, Direction.right)

        self.x = Config.playerSpawnPoint['x']
        self.y = Config.playerSpawnPoint['y']

    # game mechanics 

    def gmHandleHit(self, damage):
        self.characterStatus.getHit(damage)
        self.setColorFor( 1.0 - 1.0/damage , EntityType.takedamage)

    # /game mechanics

    def getInput(self):
        key = self.win.getch()
        while key != -1:
            if key == ord(' '):
                self.actionCtrl.changeTo(Action.hitting, self.direction)
                self.characterWeapon.doHit()

            # game related
            if key == ord('p'):
                self.world.togglePause()

            if key == 27: # esc
                self.world.quitGame()


            # player related
            if key == ord('q'):
                self.actionCtrl.changeTo(Action.shrugging, self.direction)

            if key == ord('w'):
                self.addSprite( SpeechSprite(None, parentEntity=self) )

            if key == curses.KEY_LEFT:
                if Utility.isPointMovable(self.x - 1, self.y, self.sprite.width, self.sprite.height):
                    self.x = self.x - 1
                    self.direction = Direction.left
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.advanceStep()

            elif key == curses.KEY_RIGHT: 
                if Utility.isPointMovable(self.x + 1, self.y, self.sprite.width, self.sprite.height):
                    self.x = self.x + 1
                    self.direction = Direction.right
                    self.actionCtrl.changeTo(Action.walking, self.direction)
                    self.advanceStep()

            elif key == curses.KEY_UP:
                if Config.moveDiagonal:
                    if Utility.isPointMovable(self.x +1 , self.y - 1, self.sprite.width, self.sprite.height):
                        self.y = self.y - 1
                        self.x = self.x + 1
                        self.actionCtrl.changeTo(Action.walking, self.direction)
                        self.advanceStep()
                else: 
                    if Utility.isPointMovable(self.x, self.y - 1, self.sprite.width, self.sprite.height):
                        self.y = self.y - 1
                        self.actionCtrl.changeTo(Action.walking, self.direction)
                        self.advanceStep()

            elif key == curses.KEY_DOWN: 
                if Config.moveDiagonal:
                    if Utility.isPointMovable(self.x - 1, self.y + 1, self.sprite.width, self.sprite.height):
                        self.y = self.y + 1
                        self.x = self.x - 1
                        self.actionCtrl.changeTo(Action.walking, self.direction)
                        self.advanceStep()
                    else:
                        if Utility.isPointMovable(self.x, self.y + 1, self.sprite.width, self.sprite.height):
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

        
