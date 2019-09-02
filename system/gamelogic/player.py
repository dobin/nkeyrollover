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
from sprite.coordinates import Coordinates, ExtCoordinates
from world.viewport import Viewport
#from world.world import World
#from entity.entity import Entity
from utilities.timer import Timer
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.color import Color
from texture.character.charactertype import CharacterType
from messaging import messaging, Messaging, Message, MessageType

import system.advanceable 
import system.renderable

from enum import Enum 


class PlayerState(Enum): 
    spawn = 0
    walking = 1
    
    dying = 2
    idle = 3

    attacking = 4
    attackskill = 5



class Player():
    def __init__(self):
        self.characterStatus = CharacterStatus()
        self.name = 'Player'
        self.points = 0
        self.state = PlayerState.spawn


    def advance(self, deltaTime :float):
        self.characterStatus.advance(deltaTime)


    def __repr__(self):
        return "Player"
