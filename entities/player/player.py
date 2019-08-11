#!/usr/bin/env python

import curses
import logging
from enum import Enum

from ai.brain import Brain
import entities.player.playerfsm as playerfsm
from world.particleeffecttype import ParticleEffectType
from utilities.utilities import Utility
from config import Config
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
from world.viewport import Viewport
#from world.world import World
#from entity.entity import Entity
from utilities.timer import Timer

logger = logging.getLogger(__name__)


class Player(Character):
    def __init__(
        self, viewport :Viewport, parentEntity, 
        spawnBoundaries, world
    ):
        Character.__init__(
            self, viewport=viewport, parentEntity=parentEntity, 
            spawnBoundaries=spawnBoundaries, world=world, entityType=EntityType.player)
        
        self.texture = CharacterTexture(parentSprite=self)
        self.characterAttack = CharacterAttack(viewport=viewport, parentCharacter=self, isPlayer=True)
        self.skills = PlayerSkills(player=self)
        self.movementTimer = Timer( 1.0 / Config.movementKeysPerSec, instant=True)
        self.initAi()
        self.name = 'Player'

        self.setLocation( Coordinates(
                Config.playerSpawnPoint['x'],
                Config.playerSpawnPoint['y']
            )
        )


    def initAi(self):
        self.brain = Brain(self)

        self.brain.register(playerfsm.Idle)
        self.brain.register(playerfsm.Spawn)
        self.brain.register(playerfsm.Attack)
        self.brain.register(playerfsm.Walking)
        self.brain.push("spawn")


    # game mechanics 

    def gmHandleHit(self, damage):
        self.characterStatus.getHit(damage)
        self.setColorFor( 1.0 - 1.0/damage , EntityType.takedamage)


    def getInput(self):
        gotInput = False
        key = self.viewport.win.getch()
        while key != -1:
            gotInput = True
            self.characterStatus.handleKeyPress(time=self.world.getGameTime())
            self.handleInput(key)
            key = self.viewport.win.getch()

        return gotInput


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


    def movePlayer(self):
        # move window
        playerScreenCoords = self.viewport.getScreenCoords ( self.getLocation() )
        if playerScreenCoords.x == Config.moveBorderRight:
            self.viewport.adjustViewport(-1)
        if playerScreenCoords.x == Config.moveBorderLeft:
            self.viewport.adjustViewport(1)

        # walking animation
        self.advanceStep()

        currentState = self.brain.state
        if currentState.name == 'walking': 
            # keep him walking a bit more
            currentState.setTimer(1.0)
        else: 
            self.brain.pop()
            self.brain.push('walking')


    def handleInput(self, key):
            if key == ord(' '):
                self.brain.pop()
                self.brain.push('attack')
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

            if key == ord('c'):
                self.skills.doSkill('c')

            if key == ord('f'):
                self.skills.doSkill('f')

            if key == ord('g'):
                self.skills.doSkill('g')

            if key == ord('q'):
                self.skills.doSkill('q')

            if key == ord('w'):
                self.skills.doSkill('w')

            if key == ord('e'):
                self.skills.doSkill('e')

            if key == ord('r'):
                self.skills.doSkill('r')

            if key == curses.KEY_LEFT:
                if self.movementTimer.timeIsUp(): 
                    self.movementTimer.reset()

                    if Utility.isPointMovable(self.coordinates.x - 1, self.coordinates.y, self.texture.width, self.texture.height):
                        self.coordinates.x = self.coordinates.x - 1
                        self.direction = Direction.left
                        self.movePlayer()
                    
            elif key == curses.KEY_RIGHT: 
                if self.movementTimer.timeIsUp(): 
                    self.movementTimer.reset()                
                    if Utility.isPointMovable(self.coordinates.x + 1, self.coordinates.y, self.texture.width, self.texture.height):
                        self.coordinates.x = self.coordinates.x + 1
                        self.direction = Direction.right
                        self.movePlayer()

            elif key == curses.KEY_UP:
                if self.movementTimer.timeIsUp(): 
                    self.movementTimer.reset()                
                    if Config.moveDiagonal:
                        if Utility.isPointMovable(self.coordinates.x +1 , self.coordinates.y - 1, self.texture.width, self.texture.height):
                            self.coordinates.y = self.coordinates.y - 1
                            self.coordinates.x = self.coordinates.x + 1
                            self.movePlayer()

                    else: 
                        if Utility.isPointMovable(self.coordinates.x, self.coordinates.y - 1, self.texture.width, self.texture.height):
                            self.coordinates.y = self.coordinates.y - 1
                            self.movePlayer()

            elif key == curses.KEY_DOWN: 
                if self.movementTimer.timeIsUp(): 
                    self.movementTimer.reset()
                    if Config.moveDiagonal:
                        if Utility.isPointMovable(self.coordinates.x - 1, self.coordinates.y + 1, self.texture.width, self.texture.height):
                            self.coordinates.y = self.coordinates.y + 1
                            self.coordinates.x = self.coordinates.x - 1
                            self.movePlayer()
                    else:
                        if Utility.isPointMovable(self.coordinates.x, self.coordinates.y + 1, self.texture.width, self.texture.height):
                            self.coordinates.y = self.coordinates.y + 1
                            self.movePlayer()


    def advance(self, deltaTime):
        super(Player, self).advance(deltaTime) # advance Character part (duration, sprite)
        self.brain.update(deltaTime)
        self.skills.advance(deltaTime)
        self.movementTimer.advance(deltaTime)


    def ressurectMe(self): 
        if self.characterStatus.isAlive(): 
            return

        logger.info("Ressurect player at: " + str(self.coordinates.x) + " / " + str(self.coordinates.y))
        self.characterStatus.init()
        self.brain.pop()
        self.brain.push('spawn')


    def __repr__(self): 
        return "Player"        
