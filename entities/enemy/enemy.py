import random
import logging

from texture.character.charactertexture import CharacterTexture
from entities.player.player import Player
from sprite.direction import Direction
from entities.character import Character
from config import Config
from utilities.timer import Timer
from utilities.utilities import Utility
from entities.entitytype import EntityType
from ai.brain import Brain
import entities.enemy.aifsm as aifsm
from texture.character.characteranimationtype import CharacterAnimationType
from entities.characterattack import CharacterAttack
from .enemyinfo import EnemyInfo
from sprite.coordinates import Coordinates
from world.viewport import Viewport

logger = logging.getLogger(__name__)


class Enemy(Character):
    def __init__(self, viewport :Viewport, parent, spawnBoundaries, world, name):
        Character.__init__(self, viewport, parent, spawnBoundaries, world, EntityType.enemy)
        
        self.enemyMovement = True
        self.player = world.getPlayer()
        self.texture = CharacterTexture(
            parentSprite=self, 
            characterAnimationType=CharacterAnimationType.standing,
            head=self.getRandomHead(), 
            body=self.getRandomBody())
        self.characterAttack = CharacterAttack(viewport=viewport, parentCharacter=self, isPlayer=False)
        self.name = 'Bot' + name
        self.enemyInfo = EnemyInfo()

        self.initAi()
        self.init()


    def init(self):
        if self.spawnBoundaries is None: 
            return

        self.setLocation( Coordinates(
                self.spawnBoundaries['x'],
                random.randint(self.spawnBoundaries['min_y'], self.spawnBoundaries['max_y'])
            )
        )

        if self.coordinates.x < 0:
            self.direction = Direction.right
        else: 
            self.direction = Direction.left


    def initAi(self): 
        self.brain = Brain(self)

        self.brain.register(aifsm.Idle)
        self.brain.register(aifsm.Spawn)
        self.brain.register(aifsm.Attack)
        self.brain.register(aifsm.Chase)
        self.brain.register(aifsm.Wander)
        self.brain.register(aifsm.Dying)
        self.brain.register(aifsm.AttackWindup)
        self.brain.push("spawn")


    # Game Mechanics
    def gmKill(self): 
        self.brain.pop()
        self.brain.push("dying")


    def gmRessurectMe(self): 
        if self.characterStatus.isAlive():
            logger.warn(self.name + " Trying to ressurect enemy which is still alive")
            return

        logger.info(self.name + " Ressurect at: " + str(self.coordinates))
        self.init()
        self.characterStatus.init()

        # if death animation was deluxe, there is no frame in the sprite
        # upon spawning, and an exception is thrown
        # change following two when fixed TODO
        self.texture.changeAnimation(CharacterAnimationType.standing, self.direction)
        self.setActive(True)

        self.brain.pop()
        self.brain.push('spawn')
        

    def gmHandleHit(self, damage):
        self.characterStatus.getHit(damage)
        self.setColorFor( 1.0 - 1.0/damage , EntityType.takedamage)
        if not self.characterStatus.isAlive():
            self.brain.pop()
            self.brain.push('dying')


    def canReachPlayer(self): 
        return Utility.pointInSprite(self.characterAttack.getLocation(), self.player)


    def isPlayerClose(self):
        distance = Utility.distance(self.player.getLocation(), self.getLocation())
        if distance['sum'] < 5:
            return True
        else: 
            return False


    def advance(self, deltaTime): 
        super(Enemy, self).advance(deltaTime)
        self.brain.update(deltaTime)
        

    def __repr__(self):
        return self.name