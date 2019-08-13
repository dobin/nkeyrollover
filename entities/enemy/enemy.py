import random
import logging

import entities.enemy.aifsm as aifsm
from config import Config
from utilities.timer import Timer
from utilities.utilities import Utility
from texture.character.charactertexture import CharacterTexture
from texture.character.characteranimationtype import CharacterAnimationType
from entities.player.player import Player
from entities.characterattack import CharacterAttack
from entities.character import Character
from entities.entitytype import EntityType
from ai.brain import Brain
from sprite.coordinates import Coordinates
from sprite.direction import Direction
from world.viewport import Viewport
from .enemyinfo import EnemyInfo
from texture.character.charactertype import CharacterType

logger = logging.getLogger(__name__)


class Enemy(Character):
    def __init__(
        self, viewport :Viewport, parent, 
        world, name :str, characterType=CharacterType.stickfigure
    ):
        Character.__init__(self, viewport=viewport, parentEntity=parent, 
            world=world, entityType=EntityType.enemy)
        
        self.characterType = characterType
        self.enemyMovement = True
        self.player = world.getPlayer()
        self.texture = CharacterTexture(
            parentSprite=self, 
            characterAnimationType=CharacterAnimationType.standing,
            head=self.getRandomHead(), 
            body=self.getRandomBody(),
            characterType=self.characterType)
        self.characterAttack = CharacterAttack(viewport=viewport, parentCharacter=self, 
            isPlayer=False)
        self.name = 'Bot' + name
        self.enemyInfo = EnemyInfo()

        self.initAi()


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


    def gmRessurectMe(self, spawncoord):
        self.setLocation(spawncoord)
        logger.info(self.name + " Ressurect at: " + str(self.coordinates))
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


    def move(self, x=0, y=0):
        if x > 0:
            if self.coordinates.x < Config.columns - self.texture.width - 1:
                self.coordinates.x += 1
                
                if self.direction is not Direction.right:
                    self.direction = Direction.right
                    self.texture.changeAnimation(
                        CharacterAnimationType.walking, self.direction)  

        elif x < 0:
            if self.coordinates.x > 1:
                self.coordinates.x -= 1
                if self.direction is not Direction.left:
                    self.direction = Direction.left
                    self.texture.changeAnimation(
                        CharacterAnimationType.walking, self.direction)    

        if y > 0:
            if self.coordinates.y < Config.rows - self.texture.height - 1:
                self.coordinates.y += 1
        
        elif y < 0:
            if self.coordinates.y > 2:
                self.coordinates.y -= 1



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