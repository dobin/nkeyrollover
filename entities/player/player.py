#!/usr/bin/env python

import curses
import logging
from enum import Enum

from world.particleeffecttype import ParticleEffectType
from utilities.utilities import Utility
from config import Config
from .playeractionctrl import PlayerActionCtrl
from entities.characterstatus import CharacterStatus
from sprite.direction import Direction
from entities.character import Character
from entities.entitytype import EntityType
from texture.character.charactertexture import CharacterTexture
from texture.character.characteranimationtype import CharacterAnimationType
from entities.characterattack import CharacterAttack
from entities.weapontype import WeaponType
from .playerskills import PlayerSkills
from sprite.coordinates import Coordinates

logger = logging.getLogger(__name__)


class Player(Character):
    def __init__(self, win, parentEntity, spawnBoundaries, world):
        Character.__init__(self, win, parentEntity, spawnBoundaries, world, EntityType.player)
        
        self.actionCtrl = PlayerActionCtrl(parentEntity=self, world=world)
        self.texture = CharacterTexture(parentSprite=self)
        self.characterAttack = CharacterAttack(win=win, parentCharacter=self, isPlayer=True)
        self.skills = PlayerSkills(player=self)

        # first action is standing around
        self.actionCtrl.changeTo(CharacterAnimationType.standing, Direction.right)

        self.setLocation( Coordinates(
                Config.playerSpawnPoint['x'],
                Config.playerSpawnPoint['y']
            )
        )


    # game mechanics 

    def gmHandleHit(self, damage):
        self.characterStatus.getHit(damage)
        self.setColorFor( 1.0 - 1.0/damage , EntityType.takedamage)


    def getInput(self):
        key = self.win.getch()
        while key != -1:
            self.handleInput(key)
            key = self.win.getch()


    def announce(self, damage, particleEffectType): 
        text = ''
        if particleEffectType is ParticleEffectType.laser:
            text = 'Cowabunga!'

        if particleEffectType is ParticleEffectType.cleave:
            text = 'I\'ll be back!'

        if particleEffectType is ParticleEffectType.explosion:
            text = 'Boom baby!'


        if damage > Config.announceDamage: 
            self.speechTexture.changeAnimation(text)


    def handleInput(self, key):
            if key == ord(' '):
                self.actionCtrl.changeTo(CharacterAnimationType.hitting, self.direction)
                self.characterAttack.attack()

            # game related
            if key == ord('p'):
                self.world.togglePause()

            if key == 27: # esc
                self.world.quitGame()


            # player related
            if key == ord('1'):
                self.characterAttack.switchWeaponByKey('1')

            if key == ord('2'):
                self.characterAttack.switchWeaponByKey('2')

            if key == ord('3'):
                self.characterAttack.switchWeaponByKey('3')

            if key == ord('4'):
                self.characterAttack.switchWeaponByKey('4')

            if key == ord('q'):
                self.skills.doSkill('q')

            if key == ord('w'):
                self.skills.doSkill('w')

            if key == ord('e'):
                self.skills.doSkill('e')

            if key == ord('r'):
                self.skills.doSkill('r')

            if key == curses.KEY_LEFT:
                if Utility.isPointMovable(self.coordinates.x - 1, self.coordinates.y, self.texture.width, self.texture.height):
                    self.coordinates.x = self.coordinates.x - 1
                    self.direction = Direction.left
                    self.actionCtrl.changeTo(CharacterAnimationType.walking, self.direction)
                    self.advanceStep()

            elif key == curses.KEY_RIGHT: 
                if Utility.isPointMovable(self.coordinates.x + 1, self.coordinates.y, self.texture.width, self.texture.height):
                    self.coordinates.x = self.coordinates.x + 1
                    self.direction = Direction.right
                    self.actionCtrl.changeTo(CharacterAnimationType.walking, self.direction)
                    self.advanceStep()

            elif key == curses.KEY_UP:
                if Config.moveDiagonal:
                    if Utility.isPointMovable(self.coordinates.x +1 , self.coordinates.y - 1, self.texture.width, self.texture.height):
                        self.coordinates.y = self.coordinates.y - 1
                        self.coordinates.x = self.coordinates.x + 1
                        self.actionCtrl.changeTo(CharacterAnimationType.walking, self.direction)
                        self.advanceStep()
                else: 
                    if Utility.isPointMovable(self.coordinates.x, self.coordinates.y - 1, self.texture.width, self.texture.height):
                        self.coordinates.y = self.coordinates.y - 1
                        self.actionCtrl.changeTo(CharacterAnimationType.walking, self.direction)
                        self.advanceStep()

            elif key == curses.KEY_DOWN: 
                if Config.moveDiagonal:
                    if Utility.isPointMovable(self.coordinates.x - 1, self.coordinates.y + 1, self.texture.width, self.texture.height):
                        self.coordinates.y = self.coordinates.y + 1
                        self.coordinates.x = self.coordinates.x - 1
                        self.actionCtrl.changeTo(CharacterAnimationType.walking, self.direction)
                        self.advanceStep()
                else:
                    if Utility.isPointMovable(self.coordinates.x, self.coordinates.y + 1, self.texture.width, self.texture.height):
                        self.coordinates.y = self.coordinates.y + 1
                        self.actionCtrl.changeTo(CharacterAnimationType.walking, self.direction)
                        self.advanceStep()


    def advance(self, deltaTime):
        super(Player, self).advance(deltaTime) # advance Character part (duration, sprite)
        self.actionCtrl.advance(deltaTime) # advance actions (duration, Action transfers)
        self.skills.advance(deltaTime)


    def ressurectMe(self): 
        if self.characterStatus.isAlive(): 
            return

        logger.info("Ressurect player at: " + str(self.coordinates.x) + " / " + str(self.coordinates.y))
        self.characterStatus.init()
        self.actionCtrl.changeTo(CharacterAnimationType.standing, None)

        
