import esper
import curses
import logging
from enum import Enum

from ai.brain import Brain
from world.particleeffecttype import ParticleEffectType
from utilities.utilities import Utility
from config import Config
from entities.characterstatus import CharacterStatus
from sprite.direction import Direction
from entities.character import Character
from entities.entitytype import EntityType
from texture.character.charactertexture import CharacterTexture
from texture.character.characteranimationtype import CharacterAnimationType
from entities.weapontype import WeaponType
from entities.player.playerskills import PlayerSkills
from sprite.coordinates import Coordinates, ExtCoordinates
from world.viewport import Viewport
#from world.world import World
#from entity.entity import Entity
from utilities.timer import Timer
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.color import Color
from entities.player.state_attack import StateAttack
from entities.player.state_dying import StateDying
from entities.player.state_idle import StateIdle
from entities.player.state_spawn import StateSpawn
from entities.player.state_walking import StateWalking
from texture.character.charactertype import CharacterType
from texture.speechtexture import SpeechTexture
from messaging import messaging, Messaging, Message, MessageType

import system.advanceable 
import system.renderable


class Player():
    def __init__(self, esperData):
        self.esperData = esperData

        # from character
        self.characterStatus = CharacterStatus()
        self.speechTexture = SpeechTexture(parentSprite=self, displayText='')
        self.speechTexture.setActive(False)

        # from player
        self.skills = PlayerSkills(player=self)
        self.initAi()
        self.name = 'Player'


    def initAi(self):
        self.brain = Brain(self.esperData)
        self.brain.register(StateIdle)
        self.brain.register(StateSpawn)
        self.brain.register(StateAttack)
        self.brain.register(StateWalking)
        self.brain.push("spawn")


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


    def advance(self, deltaTime):
        self.characterStatus.advance(deltaTime)
        self.speechTexture.advance(deltaTime)        
        self.brain.update(deltaTime)
        self.skills.advance(deltaTime)


    def __repr__(self): 
        return "Player"        
