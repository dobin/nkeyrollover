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
from texture.texture import Texture
from system.advanceable import Advanceable
from system.renderable import Renderable
from entities.characterstatus import CharacterStatus

logger = logging.getLogger(__name__)

class tEnemy():
    def __init__(self, player, name, renderable):
        self.enemyMovement :bool = True
        self.player = player
        self.renderable = renderable

        # CharacterAttack
        #self.characterAttack :CharacterAttack = CharacterAttack(
        #    viewport=viewport, parentCharacter=self, isPlayer=False)
        #characterAttackEntity = self.world.esperWorld.create_entity()
        #self.world.esperWorld.add_component(characterAttackEntity, Renderable(r=self.characterAttack))
        #self.world.esperWorld.add_component(characterAttackEntity, Advanceable(r=self.characterAttack))
        # /CharacterAttack 

        self.characterStatus = CharacterStatus()

        self.name :str = 'Bot' + name
        self.active = False
        self.initAi()


    def initAi(self): 
        self.brain :Brain = Brain(self.renderable)

        self.brain.register(StateIdle)
        self.brain.register(StateSpawn)
        self.brain.register(StateAttack)
        self.brain.register(StateChase)
        self.brain.register(StateWander)
        self.brain.register(StateDying)
        self.brain.register(StateAttackWindup)
        self.brain.push("idle")


    def canAttackPlayer(self) -> bool: 
        return
        hitLocations = self.characterAttack.texture.getTextureHitCoordinates()

        # only one of the hitlocations need to hit
        for hitLocation in hitLocations:
            canAttack = Utility.pointInSprite(
                hitLocation, 
                self.player)

            if canAttack: 
                return True

        return False


    def advance(self, deltaTime :float): 
        self.brain.update(deltaTime)
        #self.characterAttack.advance(deltaTime)


    def setActive(self, active :bool): 
        self.active = active


    def isActive(self) -> bool: 
        return self.active


    def __repr__(self):
        return self.name


class tEnemyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        for ent, player in self.world.get_component(tEnemy):
            player.advance(deltaTime)                