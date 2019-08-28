import random
import logging

from entities.weapontype import WeaponType
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
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.color import Color
from .state_attack import StateAttack
from .state_attackwindup import StateAttackWindup
from .state_chase import StateChase
from .state_dying import StateDying
from .state_idle import StateIdle
from .state_spawn import StateSpawn
from .state_wander import StateWander
from texture.texture import Texture
from system.advanceable import Advanceable
from system.renderable import Renderable

logger = logging.getLogger(__name__)


class Enemy(Character):
    def __init__(
        self, viewport :Viewport, parent, 
        world, name :str, characterType=CharacterType.stickfigure
    ):
        Character.__init__(self, viewport=viewport, parentEntity=parent, 
            world=world, entityType=EntityType.enemy)
        
        self.characterType :CharacterType = characterType
        self.enemyMovement :bool = True
        self.player :Player = world.getPlayer()
        self.texture :Texture = CharacterTexture(
            parentSprite=self, 
            characterAnimationType=CharacterAnimationType.standing,
            head=self.getRandomHead(), 
            body=self.getRandomBody(),
            characterType=self.characterType)

        # CharacterAttack
        self.characterAttack :CharacterAttack = CharacterAttack(
            viewport=viewport, parentCharacter=self, isPlayer=False)
        characterAttackEntity = self.world.esperWorld.create_entity()
        self.world.esperWorld.add_component(characterAttackEntity, Renderable(r=self.characterAttack))
        self.world.esperWorld.add_component(characterAttackEntity, Advanceable(r=self.characterAttack))
        # /CharacterAttack 

        self.name :str = 'Bot' + name
        self.enemyInfo :EnemyInfo = EnemyInfo()

        self.initAi()


    def initAi(self): 
        self.brain :Brain = Brain(self)

        self.brain.register(StateIdle)
        self.brain.register(StateSpawn)
        self.brain.register(StateAttack)
        self.brain.register(StateChase)
        self.brain.register(StateWander)
        self.brain.register(StateDying)
        self.brain.register(StateAttackWindup)
        self.brain.push("spawn")


    # Game Mechanics
    def gmRessurectMe(self, spawncoord :Coordinates):
        self.setLocation(spawncoord)
        logger.info(self.name + " Ressurect at: " + str(self.coordinates))
        self.characterStatus.init()

        # if death animation was deluxe, there is no frame in the sprite
        # upon spawning, and an exception is thrown
        # change following two when fixed TODO
        self.texture.changeAnimation(CharacterAnimationType.standing, self.direction)
        
        # select a weapon
        self.characterAttack.switchWeapon( random.choice( 
            [ WeaponType.hit, WeaponType.hitSquare, WeaponType.hitLine]
        ))
        self.setActive(True)

        self.brain.pop()
        self.brain.push('spawn')
        

    def gmHandleHit(self, damage :int):
        """Handle if i (the enemy) is being hit"""
        self.characterStatus.getHit(damage)
        self.setOverwriteColorFor( 
            1.0 - 1.0/damage , ColorPalette.getColorByColor(Color.red))
        if not self.characterStatus.isAlive():
            self.brain.pop()
            self.brain.push('dying')


    def move(self, x :int =0, y :int =0):
        """Move this enemy in x/y direction, if allowed. Update direction too"""
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


    def canAttackPlayer(self) -> bool: 
        hitLocations = self.characterAttack.texture.getTextureHitCoordinates()

        # only one of the hitlocations need to hit
        for hitLocation in hitLocations:
            canAttack = Utility.pointInSprite(
                hitLocation, 
                self.player)

            if canAttack: 
                return True

        return False


    def isPlayerClose(self) -> bool:
        distance = Utility.distance(self.player.getLocation(), self.getLocation())
        if distance['sum'] < 5:
            return True
        else: 
            return False


    def advance(self, deltaTime :float): 
        super(Enemy, self).advance(deltaTime)
        self.brain.update(deltaTime)
        

    def __repr__(self):
        return self.name