from enum import Enum 
import logging

from utilities.recordholder import RecordHolder
from sprite.coordinates import Coordinates
from utilities.timer import Timer
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from config import Config
from .entity import Entity
from .entitytype import EntityType
from .character import Character
from sprite.direction import Direction
from .character import Character
from .weapontype import WeaponType
from world.viewport import Viewport
from typing import List

logger = logging.getLogger(__name__)


class CharacterAttack(Entity): 
    def __init__(
        self, viewport :Viewport, parentCharacter :Character, isPlayer :bool
    ):
        super(CharacterAttack, self).__init__(
            viewport=viewport, parentSprite=parentCharacter, 
            entityType=EntityType.weapon)

        self.isPlayer :bool = isPlayer
        self.texture :PhenomenaTexture = PhenomenaTexture(phenomenaType=PhenomenaType.hit, parentSprite=self)
        self.parentCharacter :Character = parentCharacter

        # the duration of the hitting animation
        self.durationTimer.setTimer( self.texture.getAnimationTime() )
        self.durationTimer.reset()

        self.cooldownTimer :Timer =Timer(Config.playerAttacksCd, instant=True)

        self.setActive(False)
        self.weaponType :WeaponType = WeaponType.hit
        self.selectedWeaponKey :str = '1'
        

    def switchWeaponByKey(self, key :str):
        self.selectedWeaponKey = key
        if key == '1':
            self.switchWeapon(WeaponType.hit)

        if key == '2':
            self.switchWeapon(WeaponType.hitSquare)

        if key == '3':
            self.switchWeapon(WeaponType.hitLine)

        if key == '4':
            self.switchWeapon(WeaponType.jumpKick)


    def switchWeapon(self, weaponType :WeaponType):
        logger.info("Switch to weaopn: " + str(weaponType))
        self.weaponType = weaponType


    def getLocation(self) -> Coordinates: 
        baselocation = super(CharacterAttack, self).getLocation()

        xx = None
        if self.parentSprite.direction is Direction.right:
            xx = 1
        else: 
            xx = -1

        # new 1-pt weapon location
        charHalfWidth = int(self.parentCharacter.texture.width / 2.0)
        charHalfHeight = int( float(self.parentCharacter.texture.height) / 2.0)
        baselocation.y += charHalfHeight
        if self.parentSprite.direction is Direction.left: 
            baselocation.x -= 1
        else: 
            baselocation.x += self.parentCharacter.texture.width

        # adjust for weapon area
        if self.weaponType is WeaponType.hit:
            pass # all good

        elif self.weaponType is WeaponType.hitSquare: 
            baselocation.y -= 1 # move it up one notch

            if self.parentSprite.direction is Direction.left:
                baselocation.x -= self.texture.width - 1

        elif self.weaponType is WeaponType.hitLine: 
            if self.parentSprite.direction is Direction.left:
                baselocation.x -= self.texture.width - 1

        return baselocation


    def attackWeaponHit(self) -> int:
        self.texture.changeAnimation(PhenomenaType.hit, self.parentSprite.direction)
        
        # take hit locations from texture
        hitLocations = self.texture.getTextureHitCoordinates()

        damage = self.hitCollisionDetection( hitLocations )
        return damage        


    def attackWeaponHitSquare(self) -> int:
        self.texture.changeAnimation(PhenomenaType.hitSquare, self.parentSprite.direction)
        
        # take hit locations from texture
        hitLocations = self.texture.getTextureHitCoordinates()

        damage = self.hitCollisionDetection( hitLocations )
        return damage


    def attackWeaponHitLine(self) -> int: 
        self.texture.changeAnimation(PhenomenaType.hitLine, self.parentSprite.direction)
        
        # take hit locations from texture
        hitLocations = self.texture.getTextureHitCoordinates()

        damage = self.hitCollisionDetection( hitLocations )
        return damage


    def attackWeaponJumpKick(self) -> int: 
        self.texture.changeAnimation(PhenomenaType.hit, self.parentSprite.direction)
        return 0


    def attack(self):
        if not self.cooldownTimer.timeIsUp():
            RecordHolder.recordPlayerAttackCooldown(self.weaponType, time=self.cooldownTimer.getTimeLeft())
            return
        self.cooldownTimer.reset() # activate cooldown

        self.setActive(True)
        self.durationTimer.reset() # entity will setActive(false) when time is up

        damage = 0
        if self.weaponType is WeaponType.hit:
            damage = self.attackWeaponHit()
        elif self.weaponType is WeaponType.hitSquare:
            damage = self.attackWeaponHitSquare()
        elif self.weaponType is WeaponType.hitLine: 
            damage = self.attackWeaponHitLine()
        elif self.weaponType is WeaponType.jumpKick: 
            damage = self.attackWeaponJumpKick()

        RecordHolder.recordAttack(
            weaponType=self.weaponType, damage=damage, name=self.parentCharacter.name, 
            characterType=self.parentCharacter.entityType)


    def hitCollisionDetection(self, hitLocations :List[Coordinates]) -> int:
        damageSum = 0
        if self.isPlayer:
            for hitLocation in hitLocations:
                hittedEnemies = self.parentCharacter.world.director.getEnemiesHit(hitLocation)
                for enemy in hittedEnemies:
                    damage = self.parentCharacter.characterStatus.getDamage(weaponType=self.weaponType)
                    enemy.gmHandleHit(damage)
                    self.parentCharacter.gmHandleEnemyHit(damage)
                    damageSum += damage
        else: 
            for hitLocation in hitLocations:
                hittedPlayer = self.parentCharacter.world.director.getPlayersHit(hitLocation)
                for player in hittedPlayer: 
                    damage = self.parentCharacter.characterStatus.getDamage(weaponType=self.weaponType) 
                    player.gmHandleHit(damage)
                    self.parentCharacter.gmHandleEnemyHit(damage)
                    damageSum += damage

        return damageSum


    def advance(self, deltaTime :float):
        super(CharacterAttack, self).advance(deltaTime)
        self.cooldownTimer.advance(deltaTime)


    def getWeaponStr(self): 
        return self.selectedWeaponKey