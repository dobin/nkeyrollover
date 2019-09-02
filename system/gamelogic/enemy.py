import esper
import random
import logging

from entities.weapontype import WeaponType
from config import Config
from utilities.timer import Timer
from utilities.utilities import Utility
from texture.character.charactertexture import CharacterTexture
from entities.character import Character
from entities.entitytype import EntityType
from ai.brain import Brain
from sprite.coordinates import Coordinates
from sprite.direction import Direction
from world.viewport import Viewport
from texture.character.charactertype import CharacterType
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.color import Color
from entities.enemy.state_attack import StateAttack
from entities.enemy.state_attackwindup import StateAttackWindup
from entities.enemy.state_chase import StateChase
from entities.enemy.state_dying import StateDying
from entities.enemy.state_idle import StateIdle
from entities.enemy.state_spawn import StateSpawn
from entities.enemy.state_wander import StateWander
from entities.enemy.state_stun import StateStun
from texture.texture import Texture
from entities.characterstatus import CharacterStatus
from entities.enemy.enemyinfo import EnemyInfo

logger = logging.getLogger(__name__)


class Enemy():
    def __init__(self, player, name, esperData, director, world, viewport):
        self.enemyMovement :bool = True
        self.player = player #
        self.esperData = esperData
        self.director = director #
        self.world = world #
        self.viewport = viewport #

        self.characterStatus = CharacterStatus()

        self.name :str = 'Bot' + name
        self.active = False
        self.enemyInfo :EnemyInfo = EnemyInfo()

        self.initAi()

        self.offensiveAttackEntity = None


    def initAi(self): 
        self.brain :Brain = Brain(self.esperData)

        self.brain.register(StateIdle)
        self.brain.register(StateSpawn)
        self.brain.register(StateAttack)
        self.brain.register(StateChase)
        self.brain.register(StateWander)
        self.brain.register(StateStun)
        self.brain.register(StateDying)
        self.brain.register(StateAttackWindup)
        self.brain.push("idle")


    def advance(self, deltaTime :float): 
        self.brain.update(deltaTime)


    def setActive(self, active :bool): 
        self.active = active


    def isActive(self) -> bool: 
        return self.active


    def __repr__(self):
        return self.name
